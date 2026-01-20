"""Calculate the survival rate of a population over a specified time period."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import xarray as xr

from seapopym.core import kernel, template

# WARNING check that
from seapopym.standard.attributs import survival_rate_desc
from seapopym.standard.labels import ConfigurationLabels, CoordinatesLabels, ForcingLabels

if TYPE_CHECKING:
    from seapopym.standard.types import SeapopymState


def survival_rate_bednarsek(state: SeapopymState) -> xr.Dataset:
    """Compute the survival rate based on Bednarsek et al. (2021) model.

    The survival rate is calculated using a sigmoid function of a linear combination
    of temperature and acidity (pH).
    Reference: Bednarsek et al. (2021). "Integrated Assessment of Ocean Acidification Risks to Pteropods in the Northern Hemisphere"

    Parameters
    ----------
    state : SeapopymState
        The model state containing temperature, acidity and survival rate parameters.

    Returns
    -------
    xr.Dataset
        Dataset containing the survival rate (0-1).

    """
    average_temperature = state[ForcingLabels.avg_temperature_by_fgroup]
    average_acidity = state[ForcingLabels.avg_acidity_by_fgroup]

    survival_rate_0 = state[ConfigurationLabels.survival_rate_0]
    gamma_survival_rate_acidity = state[ConfigurationLabels.gamma_survival_rate_acidity]
    gamma_survival_rate_temperature = state[ConfigurationLabels.gamma_survival_rate_temperature]

    linear_function = (
        survival_rate_0
        + gamma_survival_rate_temperature * average_temperature
        + gamma_survival_rate_acidity * average_acidity
    )
    survival_rate = np.exp(linear_function) / (1 + np.exp(linear_function))  # Sigmoid function

    return xr.Dataset({ForcingLabels.survival_rate: survival_rate})


SurvivalRateTemplate = template.template_unit_factory(
    name=ForcingLabels.survival_rate,
    attributs=survival_rate_desc,
    dims=[CoordinatesLabels.functional_group, CoordinatesLabels.time, CoordinatesLabels.Y, CoordinatesLabels.X],
)

SurvivalRateBednarsekKernel = kernel.kernel_unit_factory(
    name="survival_rate_bednarsek", template=[SurvivalRateTemplate], function=survival_rate_bednarsek
)
"""Kernel to compute survival rate using Bednarsek equation."""
