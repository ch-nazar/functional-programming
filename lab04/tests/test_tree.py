from algorithms import Node, bfs_level_order, dfs_preorder_iter, inorder, postorder, preorder


def sample_tree():
    return Node(4, left=Node(2, Node(1), Node(3)), right=Node(6, None, Node(7)))


def test_traversals():
    t = sample_tree()
    assert list(preorder(t)) == [4, 2, 1, 3, 6, 7]
    assert list(inorder(t)) == [1, 2, 3, 4, 6, 7]
    assert list(postorder(t)) == [1, 3, 2, 7, 6, 4]
    assert bfs_level_order(t) == [4, 2, 6, 1, 3, 7]
    assert dfs_preorder_iter(t) == [4, 2, 1, 3, 6, 7]


def test_empty_tree():
    assert list(preorder(None)) == []
    assert bfs_level_order(None) == []
    assert dfs_preorder_iter(None) == []
