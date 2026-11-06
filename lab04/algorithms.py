from collections import deque
from dataclasses import dataclass
from functools import lru_cache
from random import choice
from typing import Callable, Generator, Optional, Sequence


def validate_input(weights: Sequence[int], values: Sequence[int], capacity: int) -> None:
    if len(weights) != len(values):
        raise ValueError("vahy i tsinnosti maiut buty odnakovoyi dovzhyny")
    if capacity < 0:
        raise ValueError("mistkist ne mozhe buty vidyemnoyu")
    if any(weight < 0 for weight in weights):
        raise ValueError("vaha ne mozhe buty vidyemnoyu")


def knapsack_no_cache(weights: Sequence[int], values: Sequence[int], capacity: int) -> int:
    validate_input(weights, values, capacity)

    def solve(index: int, remaining: int) -> int:
        if index == len(weights):
            return 0
        without_item = solve(index + 1, remaining)
        if weights[index] > remaining:
            return without_item
        with_item = values[index] + solve(index + 1, remaining - weights[index])
        return max(without_item, with_item)

    return solve(0, capacity)


def make_solver(weights: Sequence[int], values: Sequence[int]) -> Callable[[int, int], int]:
    weights_tuple = tuple(weights)
    values_tuple = tuple(values)

    @lru_cache(maxsize=None)
    def solve(index: int, remaining: int) -> int:
        if index == len(weights_tuple):
            return 0
        without_item = solve(index + 1, remaining)
        if weights_tuple[index] > remaining:
            return without_item
        with_item = values_tuple[index] + solve(index + 1, remaining - weights_tuple[index])
        return max(without_item, with_item)

    return solve


def knapsack_cached(weights: Sequence[int], values: Sequence[int], capacity: int) -> int:
    validate_input(weights, values, capacity)
    return make_solver(weights, values)(0, capacity)


def knapsack_iterative(weights: Sequence[int], values: Sequence[int], capacity: int) -> int:
    validate_input(weights, values, capacity)
    best = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for remaining in range(capacity, weight - 1, -1):
            best[remaining] = max(best[remaining], best[remaining - weight] + value)
    return best[capacity]


def quicksort(xs: list[int]) -> list[int]:
    if len(xs) <= 1:
        return xs[:]
    pivot = choice(xs)
    left = [x for x in xs if x < pivot]
    middle = [x for x in xs if x == pivot]
    right = [x for x in xs if x > pivot]
    return quicksort(left) + middle + quicksort(right)


@dataclass(slots=True)
class Node:
    key: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None


def preorder(tree: Optional[Node]) -> Generator[int, None, None]:
    if tree is None:
        return
    yield tree.key
    yield from preorder(tree.left)
    yield from preorder(tree.right)


def inorder(tree: Optional[Node]) -> Generator[int, None, None]:
    if tree is None:
        return
    yield from inorder(tree.left)
    yield tree.key
    yield from inorder(tree.right)


def postorder(tree: Optional[Node]) -> Generator[int, None, None]:
    if tree is None:
        return
    yield from postorder(tree.left)
    yield from postorder(tree.right)
    yield tree.key


def bfs_level_order(tree: Optional[Node]) -> list[int]:
    if not tree:
        return []
    queue, result = deque([tree]), []
    while queue:
        node = queue.popleft()
        result.append(node.key)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result


def dfs_preorder_iter(tree: Optional[Node]) -> list[int]:
    if not tree:
        return []
    stack, result = [tree], []
    while stack:
        node = stack.pop()
        result.append(node.key)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result


@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n maye buty nevidyemnym")
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def fib_iter(n: int) -> int:
    if n < 0:
        raise ValueError("n maye buty nevidyemnym")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fact(n: int, acc: int = 1) -> int:
    if n <= 1:
        return acc
    return fact(n - 1, acc * n)


knapsack = knapsack_cached
