"""Functions used to generalize the usage of map_blocks function in the model.

Notes
-----
This module is used to generate a template for a new variable that can be used in a xarray.map_blocks function. The
template is based on the state of the model and the dimensions of the new variable. The template can be chunked if
needed.

### xarray documentation:

> If none of the variables in obj is backed by dask arrays, calling this function is equivalent to calling
> `func(obj, *args, **kwargs)`.

"""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

import dask.array as da
import xarray as xr
from attr import field, validators
from attrs import frozen

from seapopym.standard import coordinates
from seapopym.standard.coordinate_authority import coordinate_authority
from seapopym.standard.labels import CoordinatesLabels

if TYPE_CHECKING:
    from seapopym.standard.types import ForcingAttrs, ForcingName, SeapopymDims, SeapopymForcing, SeapopymState


@frozen(kw_only=True)
class BaseTemplate:
    """Base class for template generation.

    Implements TemplateProtocol via duck typing. This class defines the interface
    for generating xarray objects (DataArray or Dataset) that serve as templates
    for model computations.
    """

    def generate(self: BaseTemplate, state: SeapopymState) -> SeapopymForcing | SeapopymState:
        """Generate an empty xr.DataArray/Dataset.

        Parameters
        ----------
        state : SeapopymState
            The input state of the model, used to determine dimensions and coordinates.

        Returns
        -------
        SeapopymForcing | SeapopymState
            The generated template object.

        Raises
        ------
        NotImplementedError
            If the subclass does not implement this method.

        """
        msg = f"Subclass {self.__class__.__name__} must implement generate method"
        raise NotImplementedError(msg)


@frozen(kw_only=True)
class TemplateUnit(BaseTemplate):
    """A unit defining a single variable template.

    Attributes
    ----------
    name : str
        The name of the variable.
    attrs : dict
        Metadata attributes for the variable.
    dims : Iterable[str | xr.DataArray]
        Dimensions of the variable.
    chunks : dict[str, int] | None
        Chunk sizes for Dask arrays.
    dtype : type | None
        Data type of the variable.

    """

    name: ForcingName
    attrs: ForcingAttrs
    dims: Iterable[SeapopymDims | SeapopymForcing] = field(validator=validators.instance_of(Iterable))
    chunks: dict[str, int] | None = None
    dtype: type | None = field(default=None, validator=validators.optional(validators.instance_of(type)))

    @dims.validator
    def _validate_dims(self, attribute, value) -> None:
        """Check if the dimensions are either SeapopymDims or SeapopymForcing objects.

        Parameters
        ----------
        attribute : attr.Attribute
            The attribute being validated.
        value : Iterable
            The value of the attribute.

        Raises
        ------
        TypeError
            If a dimension is not a valid type.

        """
        for dim in self.dims:
            if not isinstance(dim, (CoordinatesLabels, str, xr.DataArray)):
                msg = f"Dimension {dim} must be either a SeapopymDims or SeapopymForcing object."
                raise TypeError(msg)

    def generate(self: TemplateUnit, state: SeapopymState) -> SeapopymForcing:
        """Generate a DataArray template based on the state.

        Parameters
        ----------
        state : SeapopymState
            The model state.

        Returns
        -------
        SeapopymForcing
            The generated DataArray template.

        Raises
        ------
        ValueError
            If state is missing or if a required dimension is not in the state.

        """
        for dim in self.dims:
            if isinstance(dim, (CoordinatesLabels, str)) and state is None:
                msg = "You need to provide the state of the model to generate the template."
                raise ValueError(msg)
            if isinstance(dim, (CoordinatesLabels, str)) and dim not in state.coords:
                msg = f"Dimension {dim} is not defined in the state of the model."
                raise ValueError(msg)

        coords = [dim if isinstance(dim, xr.DataArray) else state[dim] for dim in self.dims]
        coords_size = [dim.size for dim in coords]
        coords_name = [dim.name for dim in coords]
        if self.chunks is not None:
            unordered_chunks = {state[k].name: v for k, v in self.chunks.items()}
            ordered_chunks = [unordered_chunks.get(dim.name, None) for dim in coords]
        else:
            ordered_chunks = {}

        # NOTE(Jules): dask empty array initialization is faster than numpy version
        template = xr.DataArray(
            da.empty(coords_size, chunks=ordered_chunks, dtype=self.dtype),
            coords=coords,
            dims=coords_name,
            name=self.name,
            attrs=self.attrs,
        )
        ordered_template = coordinates.CoordinatesLabels.order_data(template)

        # Ensure coordinate integrity after template generation
        # Convert to dataset temporarily to validate coordinates, then extract the DataArray
        validated_dataset = coordinate_authority.ensure_coordinate_integrity(ordered_template.to_dataset())
        return validated_dataset[ordered_template.name]


def template_unit_factory(
    name: ForcingName,
    attributs: ForcingAttrs,
    dims: Iterable[SeapopymDims | SeapopymForcing],
    dtype: type | None = None,
) -> type[BaseTemplate]:
    """Create a custom TemplateUnit class.

    Parameters
    ----------
    name : str
        The name of the template unit.
    attributs : dict
        Attributes for the generated DataArray.
    dims : Iterable
        Dimensions of the DataArray.
    dtype : type, optional
        Data type.

    Returns
    -------
    type[BaseTemplate]
        A custom class inheriting from TemplateUnit.

    """

    class CustomTemplateUnit(TemplateUnit):
        def __init__(self, chunk: dict) -> None:
            super().__init__(name=name, attrs=attributs, dims=dims, chunks=chunk, dtype=dtype)

    CustomTemplateUnit.__name__ = name
    return CustomTemplateUnit


@frozen(kw_only=True)
class Template(BaseTemplate):
    """A collection of TemplateUnits defining a Dataset template.

    Attributes
    ----------
    template_unit : Iterable[TemplateUnit]
        The units to include in the template.

    """

    template_unit: Iterable[TemplateUnit]

    def generate(self: Template, state: SeapopymState) -> SeapopymState:
        """Generate a Dataset template from the contained units.

        Parameters
        ----------
        state : SeapopymState
            The model state.

        Returns
        -------
        SeapopymState
            The generated Dataset template.

        """
        results = {template.name: template.generate(state) for template in self.template_unit}
        dataset = xr.Dataset(results)

        # Ensure coordinate integrity for all coordinates in the dataset
        return coordinate_authority.ensure_coordinate_integrity(dataset)
