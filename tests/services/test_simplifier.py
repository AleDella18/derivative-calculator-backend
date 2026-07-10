from app.models import tree
from app.services.differentiator import differentiator
from app.services.simplifier import simplifier


def test_multiplication():
    expr_tree = tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x"))
    derivative = differentiator(expr_tree, "x")
    result = simplifier(derivative)
    assert result == "2"


def test_multiple_multiplications():
    expr_tree = tree.TreeNode(
        "-",
        tree.TreeNode("*", tree.TreeNode("5"), tree.TreeNode("x")),
        tree.TreeNode("*", tree.TreeNode("10"), tree.TreeNode("x")),
    )
    derivative = differentiator(expr_tree, "x")
    result = simplifier(derivative)
    assert result == "-5"


def test_division():
    expr_tree = tree.TreeNode(
        "/",
        tree.TreeNode("*", tree.TreeNode("1"), tree.TreeNode("x")),
        tree.TreeNode("*", tree.TreeNode("x"), tree.TreeNode("1")),
    )
    derivative = differentiator(expr_tree, "x")
    result = simplifier(derivative)
    assert result == "0"


def test_cos_composed():
    expr_tree = tree.TreeNode(
        "cos", None, tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2"))
    )
    derivative = differentiator(expr_tree, "x")
    result = simplifier(derivative)
    assert result == "-2*x*sin(x**2)"


def test_composed_pow():
    expr_tree = tree.TreeNode(
        "-",
        tree.TreeNode(
            "*",
            tree.TreeNode("2"),
            tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("3")),
        ),
        tree.TreeNode(
            "*",
            tree.TreeNode("5"),
            tree.TreeNode("^", tree.TreeNode("x"), tree.TreeNode("2")),
        ),
    )
    derivative = differentiator(expr_tree, "x")
    result = simplifier(derivative)
    assert result == "2*x*(3*x - 5)"


def test_division():
    expr_tree = tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("x"))
    derivative = differentiator(expr_tree, "x")
    result = simplifier(derivative)
    assert result == "-1/x**2"


def test_sin_ln():
    expr_tree = tree.TreeNode(
        "sin", None, tree.TreeNode("ln", None, tree.TreeNode("x"))
    )
    derivative = differentiator(expr_tree, "x")
    result = simplifier(derivative)
    assert result == "cos(log(x))/x"


def test_sqrt_composed():
    expr_tree = tree.TreeNode(
        "sqrt",
        None,
        tree.TreeNode(
            "-",
            tree.TreeNode(
                "*",
                tree.TreeNode("2"),
                tree.TreeNode("x"),
            ),
            tree.TreeNode("1"),
        ),
    )
    derivative = differentiator(expr_tree, "x")
    result = simplifier(derivative)
    assert result == "1/sqrt(2*x - 1)"


def test_exp_composed():
    expr_tree = tree.TreeNode(
        "exp", None, tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x"))
    )
    derivative = differentiator(expr_tree, "x")
    result = simplifier(derivative)
    assert result == "2*exp(2*x)"


def test_tan_composed():
    expr_tree = tree.TreeNode(
        "tan", None, tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x"))
    )
    derivative = differentiator(expr_tree, "x")
    result = simplifier(derivative)
    assert result == "2/cos(2*x)**2"


def test_product():
    expr_tree = tree.TreeNode(
        "*",
        tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x")),
        tree.TreeNode("exp", None, tree.TreeNode("x")),
    )
    derivative = differentiator(expr_tree, "x")
    result = simplifier(derivative)
    assert result == "2*(x + 1)*exp(x)"


def test_division():
    expr_tree = tree.TreeNode(
        "/",
        tree.TreeNode("x"),
        tree.TreeNode(
            "sqrt", None, tree.TreeNode("-", tree.TreeNode("x"), tree.TreeNode("1"))
        ),
    )
    derivative = differentiator(expr_tree, "x")
    result = simplifier(derivative)
    assert result == "(x - 2)/(2*(x - 1)**(3/2))"


def test_costant():
    expr_tree = tree.TreeNode(
        "/",
        tree.TreeNode("x"),
        tree.TreeNode(
            "sqrt", None, tree.TreeNode("-", tree.TreeNode("x"), tree.TreeNode("1"))
        ),
    )
    derivative = differentiator(expr_tree, "y")
    result = simplifier(derivative)
    assert result == "0"


def test_cos_divided_sincompodes():
    expr_tree = tree.TreeNode(
        "/",
        tree.TreeNode("cos", None, tree.TreeNode("x")),
        tree.TreeNode(
            "+", tree.TreeNode("sin", None, tree.TreeNode("x")), tree.TreeNode("1")
        ),
    )
    derivative = differentiator(expr_tree, "x")
    result = simplifier(derivative)
    assert result == "-1/(sin(x) + 1)"


def test_composed_inverse_trigonometrics():
    expr_tree = tree.TreeNode(
        "arcsin",
        None,
        tree.TreeNode(
            "arccos", None, tree.TreeNode("arctan", None, tree.TreeNode("x"))
        ),
    )
    derivative = differentiator(expr_tree, "x")
    result = simplifier(derivative)
    assert result == "-1/(sqrt(1 - arccos(arctan(x))**2)*sqrt(1 - arctan(x)**2)*(x**2 + 1))"
