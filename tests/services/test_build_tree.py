from app.services.parser import build_tree, shanting_yard
from app.models import tree


def test_multiplication():
    target = tree.TreeNode(
        "-",
        tree.TreeNode(
            "+",
            tree.TreeNode("1"),
            tree.TreeNode("*", tree.TreeNode("4"), tree.TreeNode("2")),
        ),
        tree.TreeNode("5"),
    )
    postfix = shanting_yard("1+4*2-5")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_division():
    target = tree.TreeNode(
        "-",
        tree.TreeNode(
            "+",
            tree.TreeNode("1"),
            tree.TreeNode("/", tree.TreeNode("4"), tree.TreeNode("2")),
        ),
        tree.TreeNode("5"),
    )
    postfix = shanting_yard("1+4/2-5")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_parenthesis():
    target = tree.TreeNode(
        "/",
        tree.TreeNode(
            "*",
            tree.TreeNode("a"),
            tree.TreeNode("+", tree.TreeNode("b"), tree.TreeNode("c")),
        ),
        tree.TreeNode("d"),
    )

    postfix = shanting_yard("(((a*(b+c)))/d)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_ln():
    target = tree.TreeNode(
        "+",
        tree.TreeNode(
            "*",
            tree.TreeNode("3"),
            tree.TreeNode("-", tree.TreeNode("4"), tree.TreeNode("3")),
        ),
        tree.TreeNode(
            "*", tree.TreeNode("2"), tree.TreeNode("ln", None, tree.TreeNode("x"))
        ),
    )
    postfix = shanting_yard("3*(4-3)+(2*ln(x))")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_exp():
    target = tree.TreeNode(
        "/",
        tree.TreeNode(
            "*",
            tree.TreeNode("a"),
            tree.TreeNode(
                "+", tree.TreeNode("b"), tree.TreeNode("exp", None, tree.TreeNode("x"))
            ),
        ),
        tree.TreeNode("d"),
    )
    postfix = shanting_yard("(((a*(b+exp(x))))/d)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_inverse_trigonometrics():
    target = tree.TreeNode(
        "+",
        tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x")),
        tree.TreeNode(
            "*",
            tree.TreeNode(
                "/",
                tree.TreeNode(
                    "arccos",
                    None,
                    tree.TreeNode("+", tree.TreeNode("x"), tree.TreeNode("1")),
                ),
                tree.TreeNode(
                    "arctan",
                    None,
                    tree.TreeNode("+", tree.TreeNode("2"), tree.TreeNode("x")),
                ),
            ),
            tree.TreeNode(
                "arcsin",
                None,
                tree.TreeNode("exp", None, tree.TreeNode("2")),
            ),
        ),
    )

    postfix = shanting_yard("2*x+(arccos(x+1)/arctan(2+x))*arcsin(exp(2))")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_composed():
    target = tree.TreeNode(
        "cos",
        None,
        tree.TreeNode(
            "exp",
            None,
            tree.TreeNode(
                "+",
                tree.TreeNode("*", tree.TreeNode("2"), tree.TreeNode("x")),
                tree.TreeNode(
                    "sqrt",
                    None,
                    tree.TreeNode(
                        "*",
                        tree.TreeNode("x"),
                        tree.TreeNode(
                            "exp",
                            None,
                            tree.TreeNode(
                                "+",
                                tree.TreeNode(
                                    "+",
                                    tree.TreeNode("2"),
                                    tree.TreeNode(
                                        "*", tree.TreeNode("3"), tree.TreeNode("x")
                                    ),
                                ),
                                tree.TreeNode("4"),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )

    postfix = shanting_yard("cos(exp(2*x+sqrt(x*exp(2+3*x+4))))")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_cos_divided_sincomposed():
    target = tree.TreeNode(
        "/",
        tree.TreeNode("cos", None, tree.TreeNode("x")),
        tree.TreeNode(
            "sin", None, tree.TreeNode("+", tree.TreeNode("x"), tree.TreeNode("1"))
        ),
    )
    postfix = shanting_yard("cos(x)/(sin(x+1))")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_sin_comma():
    target = tree.TreeNode(
        "sin", None, tree.TreeNode("*", tree.TreeNode("3.14159"), tree.TreeNode("x"))
    )
    postfix = shanting_yard("sin(3.14159*x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_pow_of_pow():
    target = tree.TreeNode(
        "exp",
        None,
        tree.TreeNode(
            "*", tree.TreeNode("x"), tree.TreeNode("ln", None, tree.TreeNode("x"))
        ),
    )
    postfix = shanting_yard("x^x")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_sec():
    target = tree.TreeNode(
        "/", tree.TreeNode("1"), tree.TreeNode("cos", None, tree.TreeNode("x"))
    )
    postfix = shanting_yard("sec(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_csc():
    target = tree.TreeNode(
        "/", tree.TreeNode("1"), tree.TreeNode("sin", None, tree.TreeNode("x"))
    )
    postfix = shanting_yard("csc(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_cot():
    target = tree.TreeNode(
        "/",
        tree.TreeNode("cos", None, tree.TreeNode("x")),
        tree.TreeNode("sin", None, tree.TreeNode("x")),
    )
    postfix = shanting_yard("cot(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_arcsec():
    target = tree.TreeNode(
        "arccos", None, tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("x"))
    )
    postfix = shanting_yard("arcsec(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_arccsc():
    target = tree.TreeNode(
        "arcsin", None, tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("x"))
    )
    postfix = shanting_yard("arccsc(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_arccot():
    target = tree.TreeNode(
        "arctan", None, tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("x"))
    )
    postfix = shanting_yard("arccot(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_sinh():
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
    postfix = shanting_yard("sinh(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_cosh():
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
    postfix = shanting_yard("cosh(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_tanh():
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
    postfix = shanting_yard("tanh(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_sech():
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
    postfix = shanting_yard("sech(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_csch():
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
    postfix = shanting_yard("csch(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_coth():
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
    postfix = shanting_yard("coth(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_arcsinh():
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
    postfix = shanting_yard("arcsinh(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_arccosh():
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
    postfix = shanting_yard("arccosh(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_arctanh():
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
    postfix = shanting_yard("arctanh(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_arcsech():
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
    postfix = shanting_yard("arcsech(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_arccsch():
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
    postfix = shanting_yard("arccsch(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)


def test_arccoth():
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
    postfix = shanting_yard("arccoth(x)")
    result = build_tree(postfix, "x")
    assert tree.is_same_tree(result, target)
