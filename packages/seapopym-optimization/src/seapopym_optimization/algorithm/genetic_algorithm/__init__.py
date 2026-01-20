from .evaluation_strategies import (
    AbstractEvaluationStrategy,
    DistributedEvaluation,
    ParallelEvaluation,
    SequentialEvaluation,
)
from .factory import GeneticAlgorithmFactory
from .genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmParameters
from .logbook import Logbook, LogbookCategory, LogbookIndex


# Import protocols for type checking and runtime validation
from seapopym_optimization.algorithm.protocol import (
    OptimizationAlgorithmProtocol,
    OptimizationParametersProtocol,
)

__all__ = [
    # Core classes
    "GeneticAlgorithm",
    "GeneticAlgorithmParameters",
    "GeneticAlgorithmFactory",

    # Logbook
    "Logbook",
    "LogbookCategory",
    "LogbookIndex",

    # Evaluation strategies
    "AbstractEvaluationStrategy",
    "SequentialEvaluation",
    "DistributedEvaluation",
    "ParallelEvaluation",

    # Distribution management (optional)
    "DistributionManager",

    # Protocols
    "OptimizationAlgorithmProtocol",
    "OptimizationParametersProtocol",
]

