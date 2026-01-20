"""Configuration generators for SeapoPym model variants.

This module provides configuration generators that translate optimization parameters (from DEAP genetic algorithm)
into SeapoPym model configurations. Each generator is associated with a specific model variant and functional group.

The generators act as a bridge between the optimization framework and the SeapoPym model, converting
optimized parameter values into valid SeapoPym configuration objects.

Classes
-------
NoTransportConfigurationGenerator
    Configuration generator for the no-transport model variant.
AcidityConfigurationGenerator
    Configuration generator for the acidity model variant.
PteropodBedConfigurationGenerator
    Configuration generator for the pteropods bed model variant.
PteropodBedBHConfigurationGenerator
    Configuration generator for the pteropods bed with biomass harvesting model variant.
PteropodBedBHPFTConfigurationGenerator
    Configuration generator for the pteropods bed with biomass harvesting and plant functional types model variant.

Notes
-----
Configuration generators implement the ConfigurationGeneratorProtocol and work in conjunction with
FunctionalGroup definitions to define the complete optimization problem for a SeapoPym model variant.

"""

from .acidity_configuration_generator import AcidityConfigurationGenerator
from .no_transport_configuration_generator import NoTransportConfigurationGenerator
