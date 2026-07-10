from app.models import tree


def test_equal_tree():
    root1 = tree.TreeNode(
        "+",
        tree.TreeNode(
            "*",
            tree.TreeNode("2"),
            tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2")),
        ),
        tree.TreeNode(
            "sin", tree.TreeNode("+", tree.TreeNode("x"), tree.TreeNode("1"))
        ),
    )
    root2 = tree.TreeNode(
        "+",
        tree.TreeNode(
            "*",
            tree.TreeNode("2"),
            tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2")),
        ),
        tree.TreeNode(
            "sin", tree.TreeNode("+", tree.TreeNode("x"), tree.TreeNode("1"))
        ),
    )
    assert tree.is_same_tree(root1, root2)


def test_different_tree():
    root1 = tree.TreeNode(
        "+",
        tree.TreeNode(
            "*",
            tree.TreeNode("2"),
            tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2")),
        ),
        tree.TreeNode(
            "sin", tree.TreeNode("+", tree.TreeNode("x"), tree.TreeNode("1"))
        ),
    )
    root2 = tree.TreeNode(
        "+",
        tree.TreeNode(
            "*",
            tree.TreeNode("2"),
            tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2")),
        ),
        tree.TreeNode(
            "sin", tree.TreeNode("+", tree.TreeNode("x"), tree.TreeNode("2"))
        ),
    )
    assert not (tree.is_same_tree(root1, root2))


def test_level_order_traversal():
    root = tree.TreeNode(
        "+",
        tree.TreeNode(
            "*",
            tree.TreeNode("2"),
            tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2")),
        ),
        tree.TreeNode(
            "sin", tree.TreeNode("+", tree.TreeNode("x"), tree.TreeNode("1"))
        ),
    )
    stack = tree.level_order_traversal(root)
    result = []
    for node in stack:
        result.append(node.value)

    target = ["+", "*", "sin", "2", "^", "+", "x", "2", "x", "1"]

    assert len(result) == len(target)

    for i in range(len(result)):
        if result[i] != target[i]:
            assert False

    assert True


def test_contains_diff_var():
    root = tree.TreeNode(
        "cos",
        None,
        tree.TreeNode(
            "+",
            tree.TreeNode("2"),
            tree.TreeNode(
                "+",
                tree.TreeNode("3"),
                tree.TreeNode("*", tree.TreeNode("5"), tree.TreeNode("x")),
            ),
        ),
    )
    assert tree.has_diff_var(root, "x")


def test_not_diff_var():
    root = tree.TreeNode(
        "ln",
        None,
        tree.TreeNode(
            "+",
            tree.TreeNode("2"),
            tree.TreeNode(
                "+",
                tree.TreeNode("3"),
                tree.TreeNode("*", tree.TreeNode("5"), tree.TreeNode("y")),
            ),
        ),
    )
    assert not(tree.has_diff_var(root, "x"))