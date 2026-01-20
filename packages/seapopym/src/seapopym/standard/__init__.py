"""Seapopym standard types, protocols and utilities.

Central module providing:
- Type definitions and protocols
- Coordinate management and validation
- Units and attributes handling
- CF-compliant data structures
"""

from seapopym.standard.coordinate_authority import CoordinateAuthority, coordinate_authority
from seapopym.standard.labels import ConfigurationLabels, CoordinatesLabels, ForcingLabels
from seapopym.standard.protocols import (
    ChunkParameterProtocol,
    ConfigurationProtocol,
    ForcingParameterProtocol,
    FunctionalGroupParameterProtocol,
    KernelParameterProtocol,
    ModelProtocol,
    TemplateProtocol,
)
from seapopym.standard.types import ForcingName, SeapopymDims, SeapopymForcing, SeapopymState
from seapopym.standard.units import StandardUnitsRegistry

__all__ = [
    "ChunkParameterProtocol",
    "ConfigurationLabels",
    # Protocols
    "ConfigurationProtocol",
    # Coordinate authority
    "CoordinateAuthority",
    # Labels
    "CoordinatesLabels",
    "ForcingLabels",
    "ForcingName",
    "ForcingParameterProtocol",
    "FunctionalGroupParameterProtocol",
    "KernelParameterProtocol",
    "ModelProtocol",
    "SeapopymDims",
    "SeapopymForcing",
    # Core types
    "SeapopymState",
    # Units registry
    "StandardUnitsRegistry",
    "TemplateProtocol",
    "coordinate_authority",
]
