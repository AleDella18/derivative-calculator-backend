from app.services.differentiator import differentiator
from app.models import tree


def test_plus_product():
    expression_tree = tree.TreeNode(
        "+",
        tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x")),
        tree.TreeNode("1"),
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "+",
        tree.TreeNode(
            "+",
            tree.TreeNode("*", tree.TreeNode("0"), tree.TreeNode("x")),
            tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("1")),
        ),
        tree.TreeNode("0"),
    )
    assert tree.is_same_tree(result, target)


def test_min_product():
    expression_tree = tree.TreeNode(
        "-",
        tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x")),
        tree.TreeNode("1"),
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "-",
        tree.TreeNode(
            "+",
            tree.TreeNode("*", tree.TreeNode("0"), tree.TreeNode("x")),
            tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("1")),
        ),
        tree.TreeNode("0"),
    )
    assert tree.is_same_tree(result, target)


def test_multiple_multiplications():
    expression_tree = tree.TreeNode(
        "-",
        tree.TreeNode("*", tree.TreeNode("5"), tree.TreeNode("x")),
        tree.TreeNode("*", tree.TreeNode("10"), tree.TreeNode("x")),
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "-",
        tree.TreeNode(
            "+",
            tree.TreeNode("*", tree.TreeNode("0"), tree.TreeNode("x")),
            tree.TreeNode("*", tree.TreeNode("5"), tree.TreeNode("1")),
        ),
        tree.TreeNode(
            "+",
            tree.TreeNode("*", tree.TreeNode("0"), tree.TreeNode("x")),
            tree.TreeNode("*", tree.TreeNode("10"), tree.TreeNode("1")),
        ),
    )
    assert tree.is_same_tree(result, target)


def test_division_multiplication():
    expression_tree = tree.TreeNode(
        "/",
        tree.TreeNode("x"),
        tree.TreeNode("*", tree.TreeNode("5"), tree.TreeNode("x")),
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "/",
        tree.TreeNode(
            "-",
            tree.TreeNode(
                "*",
                tree.TreeNode("1"),
                tree.TreeNode("*", tree.TreeNode("5"), tree.TreeNode("x")),
            ),
            tree.TreeNode(
                "*",
                tree.TreeNode("x"),
                tree.TreeNode(
                    "+",
                    tree.TreeNode("*", tree.TreeNode("0"), tree.TreeNode("x")),
                    tree.TreeNode("*", tree.TreeNode("5"), tree.TreeNode("1")),
                ),
            ),
        ),
        tree.TreeNode(
            "^",
            tree.TreeNode("*", tree.TreeNode("5"), tree.TreeNode("x")),
            tree.TreeNode("2"),
        ),
    )
    assert tree.is_same_tree(result, target)


def test_multiplication_pow():
    expression_tree = tree.TreeNode(
        "*",
        tree.TreeNode("5"),
        tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("4")),
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "+",
        tree.TreeNode(
            "*",
            tree.TreeNode("0"),
            tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("4")),
        ),
        tree.TreeNode(
            "*",
            tree.TreeNode("5"),
            tree.TreeNode(
                "*",
                tree.TreeNode("4"),
                tree.TreeNode(
                    "^",
                    tree.TreeNode("x"),
                    tree.TreeNode("-", tree.TreeNode("4"), tree.TreeNode("1")),
                ),
            ),
        ),
    )
    assert tree.is_same_tree(result, target)


def test_cos_sin():
    expression_tree = tree.TreeNode(
        "cos", None, tree.TreeNode("sin", None, tree.TreeNode("x"))
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "*",
        tree.TreeNode("-sin", None, tree.TreeNode("sin", None, tree.TreeNode("x"))),
        tree.TreeNode("cos", None, tree.TreeNode("x")),
    )
    assert tree.is_same_tree(result, target)


def test_sin_sin():
    expression_tree = tree.TreeNode(
        "sin", None, tree.TreeNode("sin", None, tree.TreeNode("x"))
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "*",
        tree.TreeNode("cos", None, tree.TreeNode("sin", None, tree.TreeNode("x"))),
        tree.TreeNode("cos", None, tree.TreeNode("x")),
    )
    assert tree.is_same_tree(result, target)


def test_ln_composed():
    expression_tree = tree.TreeNode(
        "ln", None, tree.TreeNode("*", tree.TreeNode("5"), tree.TreeNode("x"))
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "*",
        tree.TreeNode(
            "/",
            tree.TreeNode("1"),
            tree.TreeNode("*", tree.TreeNode("5"), tree.TreeNode("x")),
        ),
        tree.TreeNode(
            "+",
            tree.TreeNode("*", tree.TreeNode("0"), tree.TreeNode("x")),
            tree.TreeNode("*", tree.TreeNode("5"), tree.TreeNode("1")),
        ),
    )
    assert tree.is_same_tree(result, target)


def test_exp_composed():
    expression_tree = tree.TreeNode(
        "exp",
        None,
        tree.TreeNode(
            "+",
            tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x")),
            tree.TreeNode("2"),
        ),
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "*",
        tree.TreeNode(
            "exp",
            None,
            tree.TreeNode(
                "+",
                tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x")),
                tree.TreeNode("2"),
            ),
        ),
        tree.TreeNode(
            "+",
            tree.TreeNode(
                "+",
                tree.TreeNode("*", tree.TreeNode("0"), tree.TreeNode("x")),
                tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("1")),
            ),
            tree.TreeNode("0"),
        ),
    )
    assert tree.is_same_tree(result, target)


def test_sqrt_cos():
    expression_tree = tree.TreeNode(
        "sqrt", None, tree.TreeNode("cos", None, tree.TreeNode("x"))
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "*",
        tree.TreeNode(
            "*",
            tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("2")),
            tree.TreeNode(
                "^",
                tree.TreeNode("cos", None, tree.TreeNode("x")),
                tree.TreeNode(
                    "-",
                    tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("2")),
                    tree.TreeNode("1"),
                ),
            ),
        ),
        tree.TreeNode("-sin", None, tree.TreeNode("x")),
    )

    assert tree.is_same_tree(result, target)


def test_tan_composed():
    expression_tree = tree.TreeNode(
        "tan",
        None,
        tree.TreeNode(
            "+",
            tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x")),
            tree.TreeNode("1"),
        ),
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "*",
        tree.TreeNode(
            "/",
            tree.TreeNode("1"),
            tree.TreeNode(
                "^",
                tree.TreeNode(
                    "cos",
                    None,
                    tree.TreeNode(
                        "+",
                        tree.TreeNode(
                            "*",
                            tree.TreeNode("2"),
                            tree.TreeNode("x"),
                        ),
                        tree.TreeNode("1"),
                    ),
                ),
                tree.TreeNode("2"),
            ),
        ),
        tree.TreeNode(
            "+",
            tree.TreeNode(
                "+",
                tree.TreeNode("*", tree.TreeNode("0"), tree.TreeNode("x")),
                tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("1")),
            ),
            tree.TreeNode("0"),
        ),
    )
    assert tree.is_same_tree(result, target)


def test_sin_cos_sin():
    expression_tree = tree.TreeNode(
        "sin",
        None,
        tree.TreeNode("cos", None, tree.TreeNode("sin", None, tree.TreeNode("x"))),
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "*",
        tree.TreeNode(
            "cos",
            None,
            tree.TreeNode("cos", None, tree.TreeNode("sin", None, tree.TreeNode("x"))),
        ),
        tree.TreeNode(
            "*",
            tree.TreeNode("-sin", None, tree.TreeNode("sin", None, tree.TreeNode("x"))),
            tree.TreeNode("cos", None, tree.TreeNode("x")),
        ),
    )
    assert tree.is_same_tree(result, target)


def test_costant_function():
    expression_tree = tree.TreeNode(
        "sin",
        None,
        tree.TreeNode("cos", None, tree.TreeNode("sin", None, tree.TreeNode("5"))),
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode("0")
    assert tree.is_same_tree(result, target)


def test_sin_ln():
    expression_tree = tree.TreeNode(
        "sin", None, tree.TreeNode("ln", None, tree.TreeNode("x"))
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "*",
        tree.TreeNode("cos", None, tree.TreeNode("ln", None, tree.TreeNode("x"))),
        tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("x")),
    )
    assert tree.is_same_tree(result, target)


def test_product_exp():
    expression_tree = tree.TreeNode(
        "*",
        tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x")),
        tree.TreeNode("exp", None, tree.TreeNode("x")),
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "+",
        tree.TreeNode(
            "*",
            tree.TreeNode(
                "+",
                tree.TreeNode("*", tree.TreeNode("0"), tree.TreeNode("x")),
                tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("1")),
            ),
            tree.TreeNode("exp", None, tree.TreeNode("x")),
        ),
        tree.TreeNode(
            "*",
            tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x")),
            tree.TreeNode("exp", None, tree.TreeNode("x")),
        ),
    )
    assert tree.is_same_tree(result, target)


def test_arcsin():
    expression_tree = tree.TreeNode(
        "arcsin",
        None,
        tree.TreeNode("x"),
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "/",
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
    )
    assert tree.is_same_tree(result, target)


def test_arccos():
    expression_tree = tree.TreeNode(
        "arccos",
        None,
        tree.TreeNode("x"),
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "/",
        tree.TreeNode("-1"),
        tree.TreeNode(
            "sqrt",
            None,
            tree.TreeNode(
                "-",
                tree.TreeNode("1"),
                tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2")),
            ),
        ),
    )
    assert tree.is_same_tree(result, target)


def test_arctan():
    expression_tree = tree.TreeNode(
        "arctan",
        None,
        tree.TreeNode("x"),
    )
    result = differentiator(expression_tree, "x")
    target = tree.TreeNode(
        "/",
        tree.TreeNode("1"),
        tree.TreeNode(
            "+",
            tree.TreeNode("1"),
            tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2")),
        ),
)
    assert tree.is_same_tree(result, target)
