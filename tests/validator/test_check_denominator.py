from app.models import tree
from app.validator.check_denominator import is_valid_denominator


def test_simple_zero_denominator():
    expr_tree = tree.TreeNode(
        "/",
        tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x")),
        tree.TreeNode("0"),
    )
    result = is_valid_denominator(expr_tree)
    assert not (result)


def test_complex_zero_denominator():
    expr_tree = tree.TreeNode(
        "/",
        tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x")),
        tree.TreeNode(
            "-",
            tree.TreeNode(
                "+",
                tree.TreeNode("x"),
                tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x")),
            ),
            tree.TreeNode("*", tree.TreeNode("3"), tree.TreeNode("x")),
        ),
    )
    result = is_valid_denominator(expr_tree)
    assert not (result)


def test_non_diffvar_zero_denominator():
    expr_tree = tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("0"))
    result = is_valid_denominator(expr_tree)
    assert not (result)


def test_valid_denominator():
    expr_tree = tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("2"))
    result = is_valid_denominator(expr_tree)
    assert result

