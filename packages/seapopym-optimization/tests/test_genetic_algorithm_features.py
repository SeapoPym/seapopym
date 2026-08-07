"""Unit tests for the GA calibration features (SBX, early stopping, plain-Sobol init).

These fast, model-free tests cover:

* simulated binary crossover (SBX) as an alternative to two-point crossover,
* early-stopping parameters on GeneticAlgorithmParameters,
* a plain Sobol-sequence initial population (saltelli=False).
"""

from __future__ import annotations

import random

import pytest
from deap import tools

from seapopym_optimization.algorithm.genetic_algorithm import GeneticAlgorithmParameters
from seapopym_optimization.algorithm.genetic_algorithm.logbook import Logbook
from seapopym_optimization.functional_group import (
    FunctionalGroupSet,
    NoTransportFunctionalGroup,
    Parameter,
)
from seapopym_optimization.functional_group.parameter_initialization import (
    initialize_with_sobol_sampling,
    random_uniform_exclusive,
)

BASE = {"ETA": 20.0, "INDPB": 0.2, "CXPB": 0.9, "MUTPB": 1.0, "NGEN": 5, "POP_SIZE": 8}
SAMPLE_COUNT = 8  # power of 2 for the Sobol balance property


def _functional_group_set() -> FunctionalGroupSet:
    def p(name: str, lo: float, hi: float) -> Parameter:
        return Parameter(name, lo, hi, init_method=random_uniform_exclusive)

    fg = NoTransportFunctionalGroup(
        name="zooplankton",
        day_layer=0,
        night_layer=0,
        energy_transfert=p("energy_transfert", 0.0, 0.5),
        gamma_tr=p("gamma_tr", -0.25, -0.001),
        tr_0=p("tr_0", 0.001, 300.0),
        gamma_lambda_temperature=p("gamma_lambda_temperature", 0.001, 0.25),
        lambda_temperature_0=p("lambda_temperature_0", 0.001, 0.1),
    )
    return FunctionalGroupSet([fg])


# --- crossover operator -----------------------------------------------------
def test_two_point_is_the_default() -> None:
    assert GeneticAlgorithmParameters(**BASE).mate is tools.cxTwoPoint


def test_sbx_selects_simulated_binary_crossover() -> None:
    assert GeneticAlgorithmParameters(**BASE, CX_METHOD="sbx").mate is tools.cxSimulatedBinaryBounded


def test_unknown_crossover_raises() -> None:
    with pytest.raises(ValueError, match="CX_METHOD"):
        GeneticAlgorithmParameters(**BASE, CX_METHOD="nope")


def test_sbx_toolbox_mate_stays_within_bounds() -> None:
    random.seed(0)
    fg = _functional_group_set()
    params = GeneticAlgorithmParameters(**BASE, CX_METHOD="sbx", CX_ETA=15.0)
    parameters = list(fg.unique_functional_groups_parameters_ordered().values())
    toolbox = params.generate_toolbox(parameters)
    child1, child2 = toolbox.mate(*toolbox.population(n=2))
    for child in (child1, child2):
        for value, parameter in zip(child, parameters, strict=True):
            assert parameter.lower_bound <= value <= parameter.upper_bound


# --- early stopping ---------------------------------------------------------
def test_early_stopping_is_disabled_by_default() -> None:
    params = GeneticAlgorithmParameters(**BASE)
    assert params.PATIENCE is None
    assert pytest.approx(1e-3) == params.TOLERANCE
    assert params.MIN_GEN == 0


def test_early_stopping_parameters_are_stored() -> None:
    params = GeneticAlgorithmParameters(**BASE, PATIENCE=25, TOLERANCE=1e-2, MIN_GEN=20)
    assert (params.PATIENCE, params.TOLERANCE, params.MIN_GEN) == (25, 1e-2, 20)


# --- Sobol initial population ----------------------------------------------
def test_plain_sobol_returns_exact_count_within_bounds() -> None:
    fg = _functional_group_set()
    samples = initialize_with_sobol_sampling(fg, SAMPLE_COUNT, saltelli=False)
    assert len(samples) == SAMPLE_COUNT
    for name, parameter in fg.unique_functional_groups_parameters_ordered().items():
        assert (samples[name] >= parameter.lower_bound).all()
        assert (samples[name] <= parameter.upper_bound).all()


def test_saltelli_design_expands_sample_count() -> None:
    fg = _functional_group_set()
    dimension = len(fg.unique_functional_groups_parameters_ordered())
    assert len(initialize_with_sobol_sampling(fg, SAMPLE_COUNT)) == SAMPLE_COUNT * (dimension + 2)


def test_from_sobol_samples_plain_has_exact_generation_zero_size() -> None:
    fg = _functional_group_set()
    logbook = Logbook.from_sobol_samples(fg, SAMPLE_COUNT, fitness_names=["obs"], saltelli=False)
    generation_zero = logbook.index.get_level_values("Generation") == 0
    assert int(generation_zero.sum()) == SAMPLE_COUNT
