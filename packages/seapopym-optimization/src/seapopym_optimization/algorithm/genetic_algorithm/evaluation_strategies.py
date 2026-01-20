"""
Evaluation strategies for genetic algorithm.

This module defines different evaluation strategies (sequential, parallel, distributed)
using the Strategy pattern, allowing dynamic mode switching without modifying
the business logic of the genetic algorithm.
"""

from __future__ import annotations

import logging
import multiprocessing
from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from dask.distributed import Client

    from seapopym_optimization.cost_function import CostFunction

logger = logging.getLogger(__name__)


class AbstractEvaluationStrategy(ABC):
    """
    Abstract interface for evaluation strategies.

    The Strategy pattern allows defining a family of evaluation algorithms,
    encapsulating them and making them interchangeable. This allows the genetic
    algorithm to vary independently from the clients that use it.
    """

    @abstractmethod
    def evaluate(self, individuals: Sequence) -> list:
        """
        Evaluate a list of individuals.

        Parameters
        ----------
        individuals : Sequence
            List of individuals to evaluate

        Returns
        -------
        list
            List of calculated fitness values

        Raises
        ------
        NotImplementedError
            If method is not implemented in derived class

        """

    def __str__(self) -> str:
        """String representation of the strategy."""
        return self.__class__.__name__


class SequentialEvaluation(AbstractEvaluationStrategy):
    """
    Classic sequential evaluation strategy.

    Uses Python's standard map() function to evaluate
    individuals one by one sequentially.
    """

    def __init__(self, cost_function: CostFunction) -> None:
        """
        Initialize sequential evaluation strategy.

        Parameters
        ----------
        cost_function : CostFunction
            Cost function to evaluate individuals

        """
        self.cost_function = cost_function

    def evaluate(self, individuals: Sequence) -> list:
        """
        Sequential evaluation with standard map().

        Parameters
        ----------
        individuals : Sequence
            List of individuals to evaluate

        Returns
        -------
        list
            List of calculated fitness values

        """
        logger.debug("Sequential evaluation of %d individuals", len(individuals))

        # Get evaluator and parameters from cost function
        evaluator = self.cost_function.get_evaluator()
        params = self.cost_function.get_distributed_parameters()

        # Convert individuals to parameter lists
        individual_params = [list(ind) for ind in individuals]

        # Sequential map with unpacked parameters
        return [evaluator(ind, **params) for ind in individual_params]


class DistributedEvaluation(AbstractEvaluationStrategy):
    """
    Distributed evaluation strategy using Dask.

    Uses Dask client.map() with a distributed CostFunction to evaluate
    individuals across multiple workers efficiently.
    """

    def __init__(self, cost_function: CostFunction, client: Client) -> None:
        """
        Initialize distributed evaluation strategy.

        Parameters
        ----------
        cost_function : CostFunction
            Cost function with distributed data (Futures)
        client : Client
            Dask distributed client for executing distributed computations

        """
        self.cost_function = cost_function
        self.client = client

    def evaluate(self, individuals: Sequence) -> list:
        """
        Distributed evaluation using client.map() with **kwargs parameters.

        Dask automatically resolves all Futures contained in kwargs
        when they are passed to the mapped function.

        Parameters
        ----------
        individuals : Sequence
            List of individuals to evaluate

        Returns
        -------
        list
            List of calculated fitness values

        """
        logger.debug("Distributed evaluation of %d individuals", len(individuals))

        # Get evaluator and distributed parameters from cost function
        evaluator = self.cost_function.get_evaluator()
        distributed_params = self.cost_function.get_distributed_parameters()

        # Convert individuals to parameter lists
        individual_params = [list(ind) for ind in individuals]

        # Map with **kwargs - Dask resolves all Futures inside distributed_params
        futures = self.client.map(
            evaluator,
            individual_params,
            **distributed_params,  # Dask automatically resolves Futures in kwargs
        )

        # Gather results
        return self.client.gather(futures)


class ParallelEvaluation(AbstractEvaluationStrategy):
    """
    Parallel evaluation strategy using multiprocessing.

    Uses ProcessPoolExecutor to evaluate individuals in parallel
    across multiple CPU cores.
    """

    def __init__(self, cost_function: CostFunction, n_jobs: int = -1) -> None:
        """
        Initialize parallel evaluation strategy.

        Parameters
        ----------
        cost_function : CostFunction
            Cost function to evaluate individuals
        n_jobs : int, default=-1
            Number of parallel jobs. If -1, use all available CPUs.

        """
        self.cost_function = cost_function

        if n_jobs == -1:
            self.n_jobs = multiprocessing.cpu_count()
        elif n_jobs > 0:
            self.n_jobs = min(n_jobs, multiprocessing.cpu_count())
        else:
            msg = "n_jobs must be positive or -1"
            raise ValueError(msg)

    def evaluate(self, individuals: Sequence) -> list:
        """
        Parallel evaluation using multiprocessing.

        Parameters
        ----------
        individuals : Sequence
            List of individuals to evaluate

        Returns
        -------
        list
            List of calculated fitness values

        """
        logger.debug("Parallel evaluation of %d individuals using %d workers", len(individuals), self.n_jobs)

        # Get evaluator and parameters from cost function
        evaluator = self.cost_function.get_evaluator()
        params = self.cost_function.get_distributed_parameters()

        # Convert individuals to parameter lists
        individual_params = [list(ind) for ind in individuals]

        # Parallel map with executor
        with ProcessPoolExecutor(max_workers=self.n_jobs) as executor:
            futures = [executor.submit(evaluator, ind, **params) for ind in individual_params]
            return [future.result() for future in futures]
