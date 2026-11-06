from algorithms import (Node, bfs_level_order, dfs_preorder_iter, fact, fib, fib_iter, inorder, knapsack_cached,
                        knapsack_iterative, knapsack_no_cache, make_solver, postorder, preorder, quicksort)


def show_knapsack() -> None:
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7
    print("Ryukzak 0/1, mistkist", capacity)
    print("Bez keshu:", knapsack_no_cache(weights, values, capacity))
    print("Z keshem:", knapsack_cached(weights, values, capacity))
    print("Iteratyvno:", knapsack_iterative(weights, values, capacity))
    solver = make_solver(weights, values)
    solver(0, capacity)
    print("cache_info:", solver.cache_info())
    solver.cache_clear()
    print("Pislya cache_clear:", solver.cache_info())


def show_basics() -> None:
    print("quicksort:", quicksort([5, 2, 9, 1, 5, 6]))
    tree = Node(4, left=Node(2, Node(1), Node(3)), right=Node(6, None, Node(7)))
    print("preorder:", list(preorder(tree)))
    print("inorder:", list(inorder(tree)))
    print("postorder:", list(postorder(tree)))
    print("bfs:", bfs_level_order(tree))
    print("dfs iteratyvno:", dfs_preorder_iter(tree))
    print("fib(30):", fib(30), "fib_iter(30):", fib_iter(30))
    print("fact(10):", fact(10))


if __name__ == "__main__":
    show_knapsack()
    show_basics()
