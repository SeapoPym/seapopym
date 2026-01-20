"""An average temperature by fgroup computation wrapper. Use xarray.map_block."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import xarray as xr

from seapopym.core import kernel, template
from seapopym.standard.attributs import min_temperature_by_cohort_desc
from seapopym.standard.labels import ConfigurationLabels, CoordinatesLabels, ForcingLabels

if TYPE_CHECKING:
    from seapopym.standard.types import SeapopymState


def min_temperature_by_cohort(state: SeapopymState) -> xr.Dataset:
    """Define the minimal temperature of a cohort to be recruited.

    Parameters
    ----------
    state : SeapopymState
        The model state containing mean timestep, TR_0 and Gamma_TR parameters.

    Returns
    -------
    xr.Dataset
        Dataset containing minimum temperature by cohort.

    Notes
    -----
    The minimal temperature for recruitment is defined as:
    Temperature = log(Tau_r / Tau_r_0) / Gamma_Tau_r
    Which is calculated from the equation Tau_r = Tau_r_0 * exp(Gamma_Tau_r * Temperature)
    Where Tau_r is equal to the cohort age.

    """
    min_temperature = (
        np.log(state[ConfigurationLabels.mean_timestep] / state[ConfigurationLabels.tr_0])
        / state[ConfigurationLabels.gamma_tr]
    )
    # TODO(Jules):
    # Should we use the min_timestep instead of mean? It would be representative of the whole cohortes
    # and not only the last 50%.
    return xr.Dataset({ForcingLabels.min_temperature: min_temperature})


MinTemperatureByCohortTemplate = template.template_unit_factory(
    name=ForcingLabels.min_temperature,
    attributs=min_temperature_by_cohort_desc,
    dims=[CoordinatesLabels.functional_group, CoordinatesLabels.cohort],
)

MinTemperatureByCohortKernel = kernel.kernel_unit_factory(
    name="min_temperature_by_cohort", template=[MinTemperatureByCohortTemplate], function=min_temperature_by_cohort
)
"""Kernel to compute minimum temperature by cohort."""
