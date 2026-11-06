import random
import pytest

from algorithms import knapsack_no_cache, knapsack_iterative, knapsack_cached, make_solver

WEIGHTS = (1, 3, 4, 5)
VALUES = (1, 4, 5, 7)


def test_classic_example():
    assert knapsack_no_cache(WEIGHTS, VALUES, 7) == 9
    assert knapsack_cached(WEIGHTS, VALUES, 7) == 9
    assert knapsack_iterative(WEIGHTS, VALUES, 7) == 9


def test_zero_capacity():
    assert knapsack_no_cache(WEIGHTS, VALUES, 0) == 0
    assert knapsack_cached(WEIGHTS, VALUES, 0) == 0
    assert knapsack_iterative(WEIGHTS, VALUES, 0) == 0


def test_empty_items():
    assert knapsack_no_cache([], [], 10) == 0
    assert knapsack_cached([], [], 10) == 0
    assert knapsack_iterative([], [], 10) == 0


def test_no_item_fits():
    assert knapsack_cached([10, 20], [5, 6], 9) == 0


def test_all_items_fit():
    assert knapsack_cached([1, 2, 3], [10, 20, 30], 100) == 60


def test_item_exactly_at_capacity():
    assert knapsack_cached([5], [8], 5) == 8


def test_input_not_modified():
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    knapsack_cached(weights, values, 7)
    assert weights == [1, 3, 4, 5] and values == [1, 4, 5, 7]


def test_three_versions_match_on_random_data():
    random.seed(1)
    for _ in range(30):
        n = random.randint(0, 10)
        weights = [random.randint(0, 8) for _ in range(n)]
        values = [random.randint(0, 50) for _ in range(n)]
        capacity = random.randint(0, 25)
        expected = knapsack_iterative(weights, values, capacity)
        assert knapsack_no_cache(weights, values, capacity) == expected
        assert knapsack_cached(weights, values, capacity) == expected


def test_invalid_data():
    with pytest.raises(ValueError):
        knapsack_cached([1, 2], [1], 5)
    with pytest.raises(ValueError):
        knapsack_cached([1], [1], -1)
    with pytest.raises(ValueError):
        knapsack_iterative([-1], [1], 5)


def test_cache_works_and_clears():
    solver = make_solver([1] * 6, [1] * 6)
    assert solver(0, 4) == 4
    assert solver.cache_info().currsize > 0
    assert solver.cache_info().hits > 0
    solver.cache_clear()
    assert solver.cache_info().currsize == 0


def test_cache_makes_fewer_calls_than_states_without_cache():
    solver = make_solver([1] * 20, [1] * 20)
    solver(0, 10)
    assert solver.cache_info().currsize <= 20 * 11


def test_deep_recursion_fails_but_iterative_not():
    weights = [1] * 3000
    values = [2] * 3000
    with pytest.raises(RecursionError):
        knapsack_cached(weights, values, 10)
    assert knapsack_iterative(weights, values, 10) == 20
