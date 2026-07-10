from app.services.transformations import (
    transform_sec,
    transform_csc,
    transform_cot,
    transform_arcsec,
    transform_arccsc,
    transform_arccot,
    transform_sinh,
    transform_cosh,
    transform_tanh,
    transform_sech,
    transform_csch,
    transform_coth,
    transform_arcsinh,
    transform_arccosh,
    transform_arctanh,
    transform_arcsech,
    transform_arccsch,
    transform_arccoth,
)
from app.models import tree


def test_transform_sec():
    target = tree.TreeNode(
        "/", tree.TreeNode("1"), tree.TreeNode("cos", None, tree.TreeNode("x"))
    )
    node_right = tree.TreeNode("x")
    result = transform_sec(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_csc():
    target = tree.TreeNode(
        "/", tree.TreeNode("1"), tree.TreeNode("sin", None, tree.TreeNode("x"))
    )
    node_right = tree.TreeNode("x")
    result = transform_csc(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_cot():
    target = tree.TreeNode(
        "/",
        tree.TreeNode("cos", None, tree.TreeNode("x")),
        tree.TreeNode("sin", None, tree.TreeNode("x")),
    )
    node_right = tree.TreeNode("x")
    result = transform_cot(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_arcsec():
    target = tree.TreeNode(
        "arccos", None, tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("x"))
    )
    node_right = tree.TreeNode("x")
    result = transform_arcsec(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_arccsc():
    target = tree.TreeNode(
        "arcsin", None, tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("x"))
    )
    node_right = tree.TreeNode("x")
    result = transform_arccsc(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_arccot():
    target = tree.TreeNode(
        "arctan", None, tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("x"))
    )
    node_right = tree.TreeNode("x")
    result = transform_arccot(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_sinh():
    target = tree.TreeNode(
        "/",
        tree.TreeNode(
            "-",
            tree.TreeNode("exp", None, tree.TreeNode("x")),
            tree.TreeNode(
                "exp",
                None,
                tree.TreeNode(
                    "*",
                    tree.TreeNode("-", tree.TreeNode("0"), tree.TreeNode("1")),
                    tree.TreeNode("x"),
                ),
            ),
        ),
        tree.TreeNode("2"),
    )
    node_right = tree.TreeNode("x")
    result = transform_sinh(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_cosh():
    target = tree.TreeNode(
        "/",
        tree.TreeNode(
            "+",
            tree.TreeNode("exp", None, tree.TreeNode("x")),
            tree.TreeNode(
                "exp",
                None,
                tree.TreeNode(
                    "*",
                    tree.TreeNode("-", tree.TreeNode("0"), tree.TreeNode("1")),
                    tree.TreeNode("x"),
                ),
            ),
        ),
        tree.TreeNode("2"),
    )
    node_right = tree.TreeNode("x")
    result = transform_cosh(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_tanh():
    target = tree.TreeNode(
        "/",
        tree.TreeNode(
            "-",
            tree.TreeNode("exp", None, tree.TreeNode("x")),
            tree.TreeNode(
                "exp",
                None,
                tree.TreeNode("-", tree.TreeNode("0"), tree.TreeNode("x")),
            ),
        ),
        tree.TreeNode(
            "+",
            tree.TreeNode("exp", None, tree.TreeNode("x")),
            tree.TreeNode(
                "exp",
                None,
                tree.TreeNode("-", tree.TreeNode("0"), tree.TreeNode("x")),
            ),
        ),
    )
    node_right = tree.TreeNode("x")
    result = transform_tanh(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_sech():
    target = tree.TreeNode(
        "/",
        tree.TreeNode("2"),
        tree.TreeNode(
            "+",
            tree.TreeNode("exp", None, tree.TreeNode("x")),
            tree.TreeNode(
                "exp", None, tree.TreeNode("-", tree.TreeNode("0"), tree.TreeNode("x"))
            ),
        ),
    )
    node_right = tree.TreeNode("x")
    result = transform_sech(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_csch():
    target = tree.TreeNode(
        "/",
        tree.TreeNode("2"),
        tree.TreeNode(
            "-",
            tree.TreeNode("exp", None, tree.TreeNode("x")),
            tree.TreeNode(
                "exp", None, tree.TreeNode("-", tree.TreeNode("0"), tree.TreeNode("x"))
            ),
        ),
    )
    node_right = tree.TreeNode("x")
    result = transform_csch(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_coth():
    target = tree.TreeNode(
        "/",
        tree.TreeNode(
            "+",
            tree.TreeNode("exp", None, tree.TreeNode("x")),
            tree.TreeNode(
                "exp",
                None,
                tree.TreeNode("-", tree.TreeNode("0"), tree.TreeNode("x")),
            ),
        ),
        tree.TreeNode(
            "-",
            tree.TreeNode("exp", None, tree.TreeNode("x")),
            tree.TreeNode(
                "exp",
                None,
                tree.TreeNode("-", tree.TreeNode("0"), tree.TreeNode("x")),
            ),
        ),
    )
    node_right = tree.TreeNode("x")
    result = transform_coth(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_arcsinh():
    target = tree.TreeNode(
        "ln",
        None,
        tree.TreeNode(
            "+",
            tree.TreeNode("x"),
            tree.TreeNode(
                "sqrt",
                None,
                tree.TreeNode(
                    "+",
                    tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2")),
                    tree.TreeNode("1"),
                ),
            ),
        ),
    )
    node_right = tree.TreeNode("x")
    result = transform_arcsinh(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_arccosh():
    target = tree.TreeNode(
        "ln",
        None,
        tree.TreeNode(
            "+",
            tree.TreeNode("x"),
            tree.TreeNode(
                "sqrt",
                None,
                tree.TreeNode(
                    "-",
                    tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2")),
                    tree.TreeNode("1"),
                ),
            ),
        ),
    )
    node_right = tree.TreeNode("x")
    result = transform_arccosh(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_arctanh():
    target = tree.TreeNode(
        "*",
        tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("2")),
        tree.TreeNode(
            "ln",
            None,
            tree.TreeNode(
                "/",
                tree.TreeNode("+", tree.TreeNode("1"), tree.TreeNode("x")),
                tree.TreeNode("-", tree.TreeNode("1"), tree.TreeNode("x")),
            ),
        ),
    )
    node_right = tree.TreeNode("x")
    result = transform_arctanh(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_arcsech():
    target = tree.TreeNode(
        "ln",
        None,
        tree.TreeNode(
            "/",
            tree.TreeNode(
                "+",
                tree.TreeNode("1"),
                tree.TreeNode(
                    "sqrt",
                    None,
                    tree.TreeNode(
                        "-",
                        tree.TreeNode("1"),
                        tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2")),
                    ),
                ),
            ),
            tree.TreeNode("x"),
        ),
    )
    node_right = tree.TreeNode("x")
    result = transform_arcsech(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_arccsch():
    target = tree.TreeNode(
        "ln",
        None,
        tree.TreeNode(
            "/",
            tree.TreeNode(
                "+",
                tree.TreeNode("1"),
                tree.TreeNode(
                    "sqrt",
                    None,
                    tree.TreeNode(
                        "+",
                        tree.TreeNode("1"),
                        tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2")),
                    ),
                ),
            ),
            tree.TreeNode("x"),
        ),
    )
    node_right = tree.TreeNode("x")
    result = transform_arccsch(node_right)
    assert tree.is_same_tree(result, target)


def test_transform_arccoth():
    target = tree.TreeNode(
        "*",
        tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("2")),
        tree.TreeNode(
            "ln",
            None,
            tree.TreeNode(
                "/",
                tree.TreeNode(
                    "+",
                    tree.TreeNode("x"),
                    tree.TreeNode("1"),
                ),
                tree.TreeNode(
                    "-",
                    tree.TreeNode("x"),
                    tree.TreeNode("1"),
                ),
            ),
        ),
    )
    node_right = tree.TreeNode("x")
    result = transform_arccoth(node_right)
    assert tree.is_same_tree(result, target)
