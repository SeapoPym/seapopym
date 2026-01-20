"""Protocol for cost functions used in optimization."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Callable
    from numbers import Number

    from seapopym_optimization.observations.protocol import ObservationProtocol


@runtime_checkable
class CostFunctionProtocol(Protocol):
    """
    Protocol for cost functions used in optimization.

    This protocol defines the interface that cost functions must implement
    to work with the optimization algorithms. It separates the evaluation
    function from the distributed parameters to enable flexible execution
    strategies (sequential, parallel, distributed).

    The key design is based on two methods:
    - get_evaluator(): Returns the core evaluation function
    - get_distributed_parameters(): Returns parameters that may be distributed (e.g., Dask Futures)

    This separation allows evaluation strategies to handle distribution
    transparently without modifying the cost function implementation.
    """

    observations: dict[str, ObservationProtocol]

    def get_evaluator(self) -> Callable[..., tuple[Number, ...]]:
        """
        Return the evaluation function to be called on workers.

        The returned function should accept:
        - args: Individual parameters as a sequence
        - Additional keyword arguments from get_distributed_parameters()

        Returns
        -------
        Callable[..., tuple[Number, ...]]
            Function that evaluates an individual and returns a tuple of fitness values

        Examples
        --------
        >>> evaluator = cost_function.get_evaluator()
        >>> params = cost_function.get_distributed_parameters()
        >>> fitness = evaluator(individual, **params)

        """
        ...

    def get_distributed_parameters(self) -> dict[str, Any]:
        """
        Return parameters that should be distributed to workers.

        Returns a dictionary of parameters that may contain distributed
        data (e.g., Dask Futures). Evaluation strategies will handle
        these parameters appropriately based on their execution mode.

        Returns
        -------
        dict[str, Any]
            Dictionary of parameters to pass to the evaluator function

        Notes
        -----
        In distributed mode, values may be Dask Futures that will be
        automatically resolved when passed to client.map().

        Examples
        --------
        >>> params = cost_function.get_distributed_parameters()
        >>> params['forcing']  # May be a Future in distributed mode
        <ForcingParameter or Future>

        """
        ...
