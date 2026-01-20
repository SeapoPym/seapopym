"""
Factory for creating configured GeneticAlgorithm instances.

This module provides factory methods to simplify the creation
of GeneticAlgorithm instances with different evaluation strategies,
hiding configuration complexity for business users.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from dask.distributed import Client, Future

from seapopym_optimization.algorithm.genetic_algorithm.evaluation_strategies import (
    DistributedEvaluation,
    ParallelEvaluation,
    SequentialEvaluation,
)
from seapopym_optimization.algorithm.genetic_algorithm.genetic_algorithm import (
    GeneticAlgorithm,
)

if TYPE_CHECKING:
    from seapopym_optimization.algorithm.genetic_algorithm.genetic_algorithm import (
        GeneticAlgorithmParameters,
    )
    from seapopym_optimization.cost_function.protocol import CostFunctionProtocol

logger = logging.getLogger(__name__)


class GeneticAlgorithmFactory:
    """
    Factory for creating GeneticAlgorithm instances with different configurations.

    This factory simplifies genetic algorithm creation by encapsulating
    the configuration logic for evaluation strategies and distribution.

    See Also
    --------
    seapopym_optimization.algorithm.genetic_algorithm.genetic_algorithm.GeneticAlgorithm : Main GA class

    """

    @staticmethod
    def create_sequential(
        meta_parameter: GeneticAlgorithmParameters, cost_function: CostFunctionProtocol, **kwargs: Any
    ) -> GeneticAlgorithm:
        """
        Create a GA in sequential mode.

        Simplest evaluation mode, suitable for small populations
        or situations where parallelization is not necessary.

        Parameters
        ----------
        meta_parameter : GeneticAlgorithmParameters
            Genetic algorithm parameters
        cost_function : CostFunctionProtocol
            Cost function to optimize
        **kwargs
            Additional arguments for GeneticAlgorithm

        Returns
        -------
        GeneticAlgorithm
            Instance configured in sequential mode

        Examples
        --------
        >>> ga = GeneticAlgorithmFactory.create_sequential(meta_params, cost_function)
        >>> results = ga.optimize()

        """
        logger.info("Creating genetic algorithm in sequential mode")

        return GeneticAlgorithm(
            meta_parameter=meta_parameter,
            cost_function=cost_function,
            evaluation_strategy=SequentialEvaluation(cost_function),
            **kwargs,
        )

    @staticmethod
    def create_parallel(
        meta_parameter: GeneticAlgorithmParameters, cost_function: CostFunctionProtocol, n_jobs: int = -1, **kwargs: Any
    ) -> GeneticAlgorithm:
        """
        Create a GA in parallel mode using multiprocessing.

        Uses ProcessPoolExecutor to evaluate individuals across
        multiple CPU cores for improved performance.

        Parameters
        ----------
        meta_parameter : GeneticAlgorithmParameters
            Genetic algorithm parameters
        cost_function : CostFunctionProtocol
            Cost function to optimize
        n_jobs : int, default=-1
            Number of parallel jobs. If -1, use all available CPUs
        **kwargs
            Additional arguments for GeneticAlgorithm

        Returns
        -------
        GeneticAlgorithm
            Instance configured in parallel mode

        Examples
        --------
        >>> ga = GeneticAlgorithmFactory.create_parallel(meta_params, cost_function, n_jobs=4)
        >>> results = ga.optimize()

        """
        logger.info("Creating genetic algorithm in parallel mode with %d jobs", n_jobs)

        return GeneticAlgorithm(
            meta_parameter=meta_parameter,
            cost_function=cost_function,
            evaluation_strategy=ParallelEvaluation(cost_function, n_jobs=n_jobs),
            **kwargs,
        )

    @staticmethod
    def create_distributed(
        meta_parameter: GeneticAlgorithmParameters,
        cost_function: CostFunctionProtocol,
        client: Client,
        **kwargs: Any,
    ) -> GeneticAlgorithm:
        """
        Create a GA in distributed mode with Dask.

        Automatically detects if data is already distributed (Futures) and distributes
        if necessary. Uses Dask client.map() with distributed data to evaluate
        individuals across multiple workers efficiently.

        WARNING: This method modifies the cost_function in-place by replacing
        forcing and observations data with Dask Futures.

        Parameters
        ----------
        meta_parameter : GeneticAlgorithmParameters
            Genetic algorithm parameters
        cost_function : CostFunctionProtocol
            Cost function to optimize (will be modified in-place)
        client : Client
            Dask client for distributed computing
        **kwargs
            Additional arguments for GeneticAlgorithm

        Returns
        -------
        GeneticAlgorithm
            GA instance configured for distributed execution

        Raises
        ------
        TypeError
            If client is not a Dask Client instance

        Examples
        --------
        >>> from dask.distributed import Client
        >>> client = Client()
        >>> ga = GeneticAlgorithmFactory.create_distributed(
        ...     meta_params, cost_function, client
        ... )
        >>> results = ga.optimize()
        >>> client.close()

        """
        if not isinstance(client, Client):
            msg = "client must be a dask.distributed.Client instance"
            raise TypeError(msg)

        logger.info("Creating genetic algorithm in distributed mode")

        # Check forcing and distribute if necessary (modify in-place)
        if isinstance(cost_function.forcing, Future):
            logger.info("Forcing already distributed (Future detected). Using existing Future.")
        else:
            logger.info("Distributing forcing to Dask workers with broadcast=True...")
            cost_function.forcing = client.scatter(cost_function.forcing, broadcast=True)

        # Check and distribute observations dict (modify in-place)
        for name, obs in cost_function.observations.items():
            if isinstance(obs, Future):
                logger.info("Observation '%s' already distributed (Future detected). Using existing Future.", name)
            else:
                logger.info("Distributing observation '%s' to Dask workers with broadcast=True...", name)
                # Distribute the entire observation object
                cost_function.observations[name] = client.scatter(obs, broadcast=True)

        # Create distributed evaluation strategy with explicit client
        evaluation_strategy = DistributedEvaluation(cost_function, client)

        # Create and return GA instance
        return GeneticAlgorithm(
            meta_parameter=meta_parameter,
            cost_function=cost_function,
            evaluation_strategy=evaluation_strategy,
            **kwargs,
        )
