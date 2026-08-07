"""CMA-ES optimization for SeapoPym models (Hansen's reference implementation, pycma).

A drop-in alternative to ``GeneticAlgorithm``: the same constructor shape (a meta-parameter object, a
``CostFunctionProtocol`` and an ``AbstractEvaluationStrategy``) and the same ``optimize() -> Logbook``
contract, so the rest of the framework (cost functions, evaluation strategies, the ``Logbook`` and every
downstream reader) is reused unchanged. Only the search differs: a smooth, bound-constrained CMA-ES
(ask / tell) replaces the DEAP genetic loop. Parameters are searched in a normalized ``[0, 1]^D`` box
(no hard clipping, hence no boundary pile-up) and mapped back to their real bounds for evaluation.

This is what makes SeapoPym's optimization layer genuinely pluggable: ``GeneticAlgorithm`` and ``CMAES``
both satisfy ``OptimizationAlgorithmProtocol`` and share the evaluation and logging machinery.

Example
-------
>>> from seapopym_optimization.algorithm.cmaes import CMAES, CMAESParameters
>>> from seapopym_optimization.algorithm.genetic_algorithm import DistributedEvaluation
>>> cmaes = CMAES(CMAESParameters(NGEN=1000), cost_function, DistributedEvaluation(cost_function, client))
>>> logbook = cmaes.optimize()
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import cma  # pycma: Hansen's reference CMA-ES (standard termination criteria + smooth bound handling)
import numpy as np

from seapopym_optimization.algorithm.genetic_algorithm.logbook import Logbook

if TYPE_CHECKING:
    from collections.abc import Sequence
    from numbers import Number

    from pandas._typing import FilePath, WriteBuffer

    from seapopym_optimization.algorithm.genetic_algorithm.evaluation_strategies import AbstractEvaluationStrategy
    from seapopym_optimization.constraint.protocol import ConstraintProtocol
    from seapopym_optimization.cost_function.protocol import CostFunctionProtocol

logger = logging.getLogger(__name__)


@dataclass
class CMAESParameters:
    """Parameters of the CMA-ES optimizer.

    Parameters
    ----------
    NGEN : int
        Maximum number of generations (a backstop). CMA-ES normally stops earlier on its own
        convergence criteria (``TOLX`` / tolfun / conditioncov).
    SIGMA0 : float, default 0.30
        Initial step size (standard deviation) in the normalized ``[0, 1]`` search space.
    POP_SIZE : int | None, default None
        Population size (lambda). ``None`` uses the CMA-ES default ``int(4 + 3 ln D)``.
    TOLX : float, default 1e-4
        CMA-ES termination tolerance on the step size, in the normalized space.
    SEED : int | None, default None
        Seed for a reproducible restart (start point and CMA-ES sampling). ``None`` means random.
    cost_function_weight : tuple, default (-1.0,)
        Per-observation weights (negative to minimize). Normalized to ``sum(|w|) = 1`` and must match
        the number of observations of the cost function.

    """

    NGEN: int = 1000
    SIGMA0: float = 0.30
    POP_SIZE: int | None = field(default=None)
    TOLX: float = field(default=1e-4)
    SEED: int | None = field(default=None)
    cost_function_weight: tuple[Number] = (-1.0,)

    def __post_init__(self: CMAESParameters) -> None:
        """Normalize the cost-function weights to ``sum(|w|) = 1`` (as the genetic algorithm does)."""
        self.cost_function_weight = tuple(
            np.asarray(self.cost_function_weight) / np.sum(np.absolute(self.cost_function_weight))
        )


@dataclass
class CMAES:
    """CMA-ES optimizer, interchangeable with ``GeneticAlgorithm``.

    Attributes mirror ``GeneticAlgorithm`` so the two are interchangeable behind
    ``OptimizationAlgorithmProtocol``.

    Attributes
    ----------
    meta_parameter : CMAESParameters
        The CMA-ES parameters.
    cost_function : CostFunctionProtocol
        The cost function to minimize. Provides the ordered parameters (with bounds) and observations.
    evaluation_strategy : AbstractEvaluationStrategy
        Strategy used to evaluate candidates (sequential, parallel or distributed) -- identical to the
        one used by the genetic algorithm.
    constraint : Sequence[ConstraintProtocol] | None
        Not supported by this backend yet (CMA-ES enforces parameter limits via its box bounds); must
        be ``None``.
    save : path | None
        If given, the logbook is written there (Parquet) at the end of the run.
    stop_reason : str
        Set by ``optimize()``: the comma-separated CMA-ES termination criteria that ended the search
        (empty before the first run). Lets a caller distinguish a converged run from one stopped by
        the ``NGEN`` backstop.

    """

    meta_parameter: CMAESParameters
    cost_function: CostFunctionProtocol
    evaluation_strategy: AbstractEvaluationStrategy
    constraint: Sequence[ConstraintProtocol] | None = None
    save: FilePath | WriteBuffer[bytes] | None = None
    logbook: Logbook | None = field(default=None, repr=False)
    stop_reason: str = field(default="", repr=False)

    def __post_init__(self: CMAES) -> None:
        """Validate the configuration (constraints, save path, weight length)."""
        if self.constraint is not None:
            # CMA-ES enforces parameter limits via its box bounds; penalty-style constraints (as the
            # genetic algorithm applies via toolbox.decorate) are not wired into this backend yet.
            msg = "CMAES does not support penalty constraints yet; parameter limits are enforced via the CMA-ES box."
            raise NotImplementedError(msg)
        if self.save is not None:
            self.save = Path(self.save)
        n_observations = len(self.cost_function.observations)
        if len(self.meta_parameter.cost_function_weight) != n_observations:
            msg = (
                "The cost function weight must have the same length as the number of observations. "
                f"Got {len(self.meta_parameter.cost_function_weight)} and {n_observations}."
            )
            raise ValueError(msg)

    def optimize(self: CMAES) -> Logbook:
        """Run CMA-ES and return the optimization ``Logbook`` (same schema as the genetic algorithm).

        The search runs in a normalized ``[0, 1]^D`` box and each candidate is mapped back to its real
        bounds before evaluation. The scalar minimized by CMA-ES is the negative weighted fitness, so the
        ``Weighted_fitness`` stored in the logbook keeps the genetic-algorithm convention (higher = better).
        """
        parameters = self.cost_function.functional_groups.unique_functional_groups_parameters_ordered()
        names = list(parameters.keys())
        lower = np.asarray([p.lower_bound for p in parameters.values()], dtype=float)
        upper = np.asarray([p.upper_bound for p in parameters.values()], dtype=float)
        observation_names = list(self.cost_function.observations.keys())
        weights = np.asarray(self.meta_parameter.cost_function_weight, dtype=float)
        n_dim = len(names)

        def denormalize(x_norm: Sequence[float]) -> list[float]:
            return (lower + np.clip(np.asarray(x_norm, dtype=float), 0.0, 1.0) * (upper - lower)).tolist()

        # Legacy RandomState (not the modern default_rng) on purpose: it matches the original
        # experiment loop's start point so a seeded run reproduces the published products byte-for-byte.
        x0 = np.random.RandomState(self.meta_parameter.SEED).uniform(0.0, 1.0, n_dim).tolist()
        options = {
            "bounds": [0.0, 1.0],
            "maxiter": self.meta_parameter.NGEN,
            "tolx": self.meta_parameter.TOLX,
            "verbose": -9,
        }
        if self.meta_parameter.POP_SIZE is not None:
            options["popsize"] = self.meta_parameter.POP_SIZE
        if self.meta_parameter.SEED is not None:
            options["seed"] = int(self.meta_parameter.SEED) + 1  # pycma treats seed 0 as "pick a random seed"
        strategy = cma.CMAEvolutionStrategy(x0, self.meta_parameter.SIGMA0, options)

        generation = 0
        while not strategy.stop():
            candidates = strategy.ask()  # lambda candidates in [0, 1]^D (bounds handled by pycma)
            individuals = [denormalize(x) for x in candidates]
            fitnesses = [tuple(np.asarray(f, dtype=float)) for f in self.evaluation_strategy.evaluate(individuals)]
            weighted_fitness = [float(np.dot(f, weights)) for f in fitnesses]  # higher is better
            costs = [-w if np.isfinite(w) else 1e6 for w in weighted_fitness]  # CMA-ES minimizes; penalty on nan/inf
            strategy.tell(candidates, costs)

            generation_log = Logbook.from_array(
                generation=[generation] * len(individuals),
                is_from_previous_generation=[False] * len(individuals),
                individual=individuals,
                parameter_names=names,
                fitness_names=observation_names,
                fitness_values=fitnesses,
                weighted_fitness=weighted_fitness,
            )
            self.logbook = (
                generation_log if self.logbook is None else self.logbook.append_new_generation(generation_log)
            )
            generation += 1

        self.stop_reason = ",".join(sorted(strategy.stop()))
        logger.info("CMA-ES stopped after %d generations (%s).", generation, self.stop_reason)
        if self.save is not None:
            self.logbook.to_parquet(self.save)
        return self.logbook.copy()
