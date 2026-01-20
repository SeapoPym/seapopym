# Import protocols for type checking and runtime validation
from seapopym_optimization.algorithm.protocol import (
    OptimizationAlgorithmProtocol,
    OptimizationParametersProtocol,
)

from .evaluation_strategies import (
    AbstractEvaluationStrategy,
    DistributedEvaluation,
    ParallelEvaluation,
    SequentialEvaluation,
)
from .factory import GeneticAlgorithmFactory
from .genetic_algorithm import GeneticAlgorithm, GeneticAlgorithmParameters
from .logbook import Logbook, LogbookCategory, LogbookIndex

__all__ = [
    # Evaluation strategies
    "AbstractEvaluationStrategy",
    "DistributedEvaluation",
    # Distribution management (optional)
    "DistributionManager",
    # Core classes
    "GeneticAlgorithm",
    "GeneticAlgorithmFactory",
    "GeneticAlgorithmParameters",
    # Logbook
    "Logbook",
    "LogbookCategory",
    "LogbookIndex",
    # Protocols
    "OptimizationAlgorithmProtocol",
    "OptimizationParametersProtocol",
    "ParallelEvaluation",
    "SequentialEvaluation",
]
