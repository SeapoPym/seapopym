"""Configuration generators for SeapoPym model variants.

This module provides configuration generators that translate optimization parameters (from DEAP genetic algorithm)
into SeapoPym model configurations. Each generator is associated with a specific model variant and functional group.

The generators act as a bridge between the optimization framework and the SeapoPym model, converting
optimized parameter values into valid SeapoPym configuration objects.

Classes
-------
NoTransportConfigurationGenerator
    Configuration generator for the no-transport model variant.

Notes
-----
Configuration generators implement the ConfigurationGeneratorProtocol and work in conjunction with
FunctionalGroup definitions to define the complete optimization problem for a SeapoPym model variant.

"""

from .no_transport_configuration_generator import NoTransportConfigurationGenerator
