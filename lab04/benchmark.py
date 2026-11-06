import random
import sys
from timeit import timeit

from algorithms import knapsack_no_cache, knapsack_iterative, knapsack_cached, make_solver


def random_items(item_count: int):
    random.seed(15)
    weights = [random.randint(1, 20) for _ in range(item_count)]
    values = [random.randint(1, 100) for _ in range(item_count)]
    return weights, values


def compare_time() -> None:
    for item_count in (10, 15, 20):
        weights, values = random_items(item_count)
        capacity = 5 * item_count
        no_cache_time = timeit(lambda: knapsack_no_cache(weights, values, capacity), number=1)
        cached_time = timeit(lambda: knapsack_cached(weights, values, capacity), number=1)
        iter_time = timeit(lambda: knapsack_iterative(weights, values, capacity), number=1)
        print(f"n={item_count}: bez keshu {no_cache_time:.4f} s, z keshem {cached_time:.4f} s, iteratyvno {iter_time:.4f} s")


def show_cache() -> None:
    weights, values = random_items(20)
    solver = make_solver(weights, values)
    print("Rezultat:", solver(0, 100))
    print("cache_info:", solver.cache_info())
    solver.cache_clear()
    print("Pislya cache_clear:", solver.cache_info())


def show_recursion_limit() -> None:
    weights, values = random_items(5000)
    print("Limit rekursiyi CPython:", sys.getrecursionlimit())
    try:
        knapsack_cached(weights, values, 100)
    except RecursionError:
        print("Rekursivna versiya z n=5000: RecursionError")
    print("Iteratyvna versiya z n=5000:", knapsack_iterative(weights, values, 100))


if __name__ == "__main__":
    compare_time()
    show_cache()
    show_recursion_limit()
