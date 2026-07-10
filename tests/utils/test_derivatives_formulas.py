from app.utils.derivative_formulas import (
    derivative_of_costant,
    derivative_of_diffvar,
    derivative_of_plus_minus,
    derivative_of_product,
    derivative_of_division,
    derivative_of_ln,
    derivative_of_exp,
    derivative_of_pow,
    derivative_of_sqrt,
    derivative_of_sin,
    derivative_of_cos,
    derivative_of_tan,
    derivative_of_arcsin,
    derivative_of_arccos,
    derivative_of_arctan
)
from app.models import tree


def test_costant():
    target = tree.TreeNode("0")
    result = derivative_of_costant()
    assert tree.is_same_tree(target, result)


def test_diffvar():
    target = tree.TreeNode("1")
    result = derivative_of_diffvar()
    assert tree.is_same_tree(target, result)


def test_plus():
    left = tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x"))
    right = tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("3"))

    left_derivative = tree.TreeNode("2")
    right_derivative = tree.TreeNode(
        "*",
        tree.TreeNode("3"),
        tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2")),
    )

    node = tree.TreeNode("+", left, right)

    derivatives = {left: left_derivative, right: right_derivative}

    target = tree.TreeNode("+", left_derivative, right_derivative)
    result = derivative_of_plus_minus(node, derivatives)
    assert tree.is_same_tree(result, target)


def test_minus():
    left = tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x"))
    right = tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("3"))

    left_derivative = tree.TreeNode("2")
    right_derivative = tree.TreeNode(
        "*",
        tree.TreeNode("3"),
        tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2")),
    )

    node = tree.TreeNode("-", left, right)

    derivatives = {left: left_derivative, right: right_derivative}

    target = tree.TreeNode("-", left_derivative, right_derivative)
    result = derivative_of_plus_minus(node, derivatives)
    assert tree.is_same_tree(result, target)


def test_product():
    left = tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("2"))
    right = tree.TreeNode("x")

    left_derivative = derivative_of_costant()
    right_derivative = derivative_of_diffvar()

    node = tree.TreeNode("*", left, right)

    derivatives = {left: left_derivative, right: right_derivative}

    target = tree.TreeNode(
        "+",
        tree.TreeNode("*", tree.TreeNode("0"), tree.TreeNode("x")),
        tree.TreeNode(
            "*",
            tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("2")),
            tree.TreeNode("1"),
        ),
    )
    result = derivative_of_product(node, derivatives)
    assert tree.is_same_tree(result, target)


def test_derivative_pow():
    node = tree.TreeNode(
        "^",
        tree.TreeNode("+", tree.TreeNode("x"), tree.TreeNode("2")),
        tree.TreeNode("3"),
    )
    target = tree.TreeNode(
        "*",
        tree.TreeNode("3"),
        tree.TreeNode(
            "^",
            tree.TreeNode("+", tree.TreeNode("x"), tree.TreeNode("2")),
            tree.TreeNode("-", tree.TreeNode("3"), tree.TreeNode("1")),
        ),
    )
    result = derivative_of_pow(node)
    assert tree.is_same_tree(result, target)


def test_derivative_division():
    left = tree.TreeNode("1")
    right = tree.TreeNode("x")

    left_derivative = derivative_of_costant()
    right_derivative = derivative_of_diffvar()

    node = tree.TreeNode("/", left, right)

    derivatives = {left: left_derivative, right: right_derivative}

    target = tree.TreeNode(
        "/",
        tree.TreeNode(
            "-",
            tree.TreeNode("*", tree.TreeNode("0"), tree.TreeNode("x")),
            tree.TreeNode("*", tree.TreeNode("1"), tree.TreeNode("1")),
        ),
        tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2")),
    )
    result = derivative_of_division(node, derivatives)
    assert tree.is_same_tree(result, target)


def test_derivative_ln():
    node = tree.TreeNode("ln", None, tree.TreeNode("x"))
    target = tree.TreeNode("/", tree.TreeNode("1"), node.right)
    result = derivative_of_ln(node)
    assert tree.is_same_tree(result, target)


def test_derivative_exp():
    node = tree.TreeNode(
        "exp", None, tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x"))
    )
    target = node
    result = derivative_of_exp(node)
    assert tree.is_same_tree(result, target)


def test_derivative_sqrt():
    node = tree.TreeNode(
        "sqrt", None, tree.TreeNode("+", tree.TreeNode("x"), tree.TreeNode("2"))
    )
    target = tree.TreeNode(
        "*",
        tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("2")),
        tree.TreeNode(
            "^",
            tree.TreeNode("+", tree.TreeNode("x"), tree.TreeNode("2")),
            tree.TreeNode(
                "-",
                tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("2")),
                tree.TreeNode("1"),
            ),
        ),
    )

    result = derivative_of_sqrt(node)
    assert tree.is_same_tree(result, target)


def test_derivative_sin():
    node = tree.TreeNode(
        "sin", None, tree.TreeNode("+", tree.TreeNode("2"), tree.TreeNode("x"))
    )
    target = tree.TreeNode(
        "cos", None, tree.TreeNode("+", tree.TreeNode("2"), tree.TreeNode("x"))
    )
    result = derivative_of_sin(node)
    assert tree.is_same_tree(result, target)


def test_derivative_cos():
    node = tree.TreeNode(
        "cos", None, tree.TreeNode("+", tree.TreeNode("2"), tree.TreeNode("x"))
    )
    target = tree.TreeNode(
        "-sin", None, tree.TreeNode("+", tree.TreeNode("2"), tree.TreeNode("x"))
    )
    result = derivative_of_cos(node)
    assert tree.is_same_tree(result, target)


def test_derivative_tan():
    node = tree.TreeNode(
        "tan", None, tree.TreeNode("+", tree.TreeNode("2"), tree.TreeNode("x"))
    )
    target = tree.TreeNode(
        "/",
        tree.TreeNode("1"),
        tree.TreeNode(
            "^",
            tree.TreeNode(
                "cos", None, tree.TreeNode("+", tree.TreeNode("2"), tree.TreeNode("x"))
            ),
            tree.TreeNode("2"),
        ),
    )

    result = derivative_of_tan(node)
    assert tree.is_same_tree(result, target)


def test_derivative_arcsin():
    node = tree.TreeNode(
        "arcsin", None, tree.TreeNode("+", tree.TreeNode("2"), tree.TreeNode("x"))
    )
    target = tree.TreeNode(
        "/",
        tree.TreeNode("1"),
        tree.TreeNode(
            "sqrt",
            None,
            tree.TreeNode(
                "-",
                tree.TreeNode("1"),
                tree.TreeNode(
                    "^",
                    tree.TreeNode("+", tree.TreeNode("2"), tree.TreeNode("x")),
                    tree.TreeNode("2"),
                ),
            ),
        ),
    )
    result = derivative_of_arcsin(node)
    assert tree.is_same_tree(result, target)


def test_derivative_arccos():
    node = tree.TreeNode(
        "arccos", None, tree.TreeNode("+", tree.TreeNode("2"), tree.TreeNode("x"))
    )
    target = tree.TreeNode(
        "/",
        tree.TreeNode("-1"),
        tree.TreeNode(
            "sqrt",
            None,
            tree.TreeNode(
                "-",
                tree.TreeNode("1"),
                tree.TreeNode(
                    "^",
                    tree.TreeNode("+", tree.TreeNode("2"), tree.TreeNode("x")),
                    tree.TreeNode("2"),
                ),
            ),
        ),
    )
    result = derivative_of_arccos(node)
    assert tree.is_same_tree(result, target)


def test_derivative_arctan():
    node = tree.TreeNode(
        "arctan", None, tree.TreeNode("+", tree.TreeNode("2"), tree.TreeNode("x"))
    )
    target = tree.TreeNode(
        "/",
        tree.TreeNode("1"),
        tree.TreeNode(
            "+",
            tree.TreeNode("1"),
            tree.TreeNode(
                "^", tree.TreeNode("+", tree.TreeNode("2"), tree.TreeNode("x")),
                tree.TreeNode("2")
            ),
        ),
    )
    result = derivative_of_arctan(node)
    assert tree.is_same_tree(result, target)
