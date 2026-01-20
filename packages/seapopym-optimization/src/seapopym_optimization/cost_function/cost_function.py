"""This module contains the cost function used to optimize the parameters of the SeapoPym model."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from numbers import Number
    from typing import Any

    import numpy as np
    from seapopym.standard.protocols import ForcingParameterProtocol, KernelParameterProtocol

    from seapopym_optimization.configuration_generator.protocols import ConfigurationGeneratorProtocol
    from seapopym_optimization.cost_function.processor import AbstractScoreProcessor
    from seapopym_optimization.functional_group.base_functional_group import AbstractFunctionalGroup, FunctionalGroupSet
    from seapopym_optimization.observations.protocol import ObservationProtocol

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class CostFunction:
    """The cost function generator for SeapoPym models."""

    # TODO(Jules): We can gather configuration generators and functional groups in a single object later if needed.
    configuration_generator: ConfigurationGeneratorProtocol
    functional_groups: FunctionalGroupSet[AbstractFunctionalGroup]
    forcing: ForcingParameterProtocol
    kernel: KernelParameterProtocol
    observations: dict[str, ObservationProtocol] | Sequence[ObservationProtocol]  # Dict or Sequence of observations
    processor: AbstractScoreProcessor  # Processor for computing scores from state and observations

    def __post_init__(self: CostFunction) -> None:
        """Convert observations to dict if needed and validate observation names match dictionary keys."""
        # Convert Sequence to dict if needed
        if not isinstance(self.observations, dict):
            self.observations = {obs.name: obs for obs in self.observations}

        # Validate that observation names match dictionary keys
        for name, obs in self.observations.items():
            if obs.name != name:
                msg = f"Observation name mismatch: key='{name}', obs.name='{obs.name}'"
                raise ValueError(msg)

    # NOTE(Jules): Forcing and observations must be passed as parameter of the cost function to be used with Dask
    # and scattered to workers. They cannot be attributes of the class.
    def _cost_function(
        self: CostFunction,
        args: np.ndarray,
        forcing: ForcingParameterProtocol,
        observations: dict[str, ObservationProtocol],
    ) -> tuple:
        """
        Evaluate the cost function for given parameters.

        Parameters
        ----------
        args : np.ndarray
            Individual parameters to evaluate
        forcing : ForcingParameterProtocol
            Forcing parameters (resolved from Future if distributed)
        observations : dict[str, ObservationProtocol]
            Dictionary of observations (resolved from Futures if distributed)

        Returns
        -------
        tuple
            Fitness values for each observation (in dict order)

        """
        configuration = self.configuration_generator.generate(
            functional_group_parameters=self.functional_groups.generate(args),
            forcing_parameters=forcing,
            kernel=self.kernel,
        )

        # Create model from configuration and run it
        with self.configuration_generator.model_class.from_configuration(configuration) as model:
            model.run()
            state = model.state

            # Compute score for each observation (dict preserves insertion order in Python 3.7+)
            return tuple(self.processor.process(state, obs) for obs in observations.values())

    def get_evaluator(self: CostFunction) -> Callable[..., tuple[Number, ...]]:
        """
        Return the evaluation function to be called on workers.

        This method is used by distributed evaluation strategies to obtain
        the core evaluation function without captured parameters.

        Returns
        -------
        Callable[..., tuple[Number, ...]]
            Function that takes (args, forcing, observations) and returns a tuple of fitness values

        Examples
        --------
        >>> evaluator = cost_function.get_evaluator()
        >>> fitness = evaluator(args, forcing_data, observations_data)

        """
        return self._cost_function

    def get_distributed_parameters(self: CostFunction) -> dict[str, Any]:
        """
        Return parameters that should be distributed to workers as a dictionary.

        Dask will automatically resolve any Futures contained in this dictionary
        when it's passed as an argument to client.map().

        Returns
        -------
        dict[str, Any]
            Dictionary with keys:
            - 'forcing': ForcingParameter or Future
            - 'observations': Dict of observations {name: observation} or {name: Future}

        Notes
        -----
        If you subclass CostFunction and add new distributed parameters,
        override this method to include them in the returned dictionary.

        Examples
        --------
        >>> params = cost_function.get_distributed_parameters()
        >>> params['forcing']
        <ForcingParameter or Future>
        >>> params['observations']
        {'Biomass': <TimeSeriesObservation or Future>, ...}

        See Also
        --------
        get_evaluator : Get the evaluation function to use with these parameters

        """
        return {
            "forcing": self.forcing,
            "observations": self.observations,
        }
