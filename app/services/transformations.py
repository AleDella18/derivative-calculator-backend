from app.models import tree


# Transforms the sec function in a more suitable form.
# @param node_right: the argument of the sec function.
# @return: An expression tree that represents the sec function in a more suitable form.
def transform_sec(node_right):
    return tree.TreeNode(
        "/", tree.TreeNode("1"), tree.TreeNode("cos", None, node_right)
    )


# Transforms the csc function in a more suitable form.
# @param node_right: the argument of the csc function.
# @return: An expression tree that represents the csc function in a more suitable form.
def transform_csc(node_right):
    return tree.TreeNode(
        "/", tree.TreeNode("1"), tree.TreeNode("sin", None, node_right)
    )


# Transforms the cot function in a more suitable form.
# @param node_right: the argument of the cot function.
# @return: An expression tree that represents the cot function in a more suitable form.
def transform_cot(node_right):
    return tree.TreeNode(
        "/",
        tree.TreeNode("cos", None, node_right),
        tree.TreeNode("sin", None, node_right),
    )


# Transforms the arcsec function in a more suitable form.
# @param node_right: the argument of the arcsec function.
# @return: An expression tree that represents the arcsec function in a more suitable form.
def transform_arcsec(node_right):
    return tree.TreeNode(
        "arccos", None, tree.TreeNode("/", tree.TreeNode("1"), node_right)
    )


# Transforms the arccsc function in a more suitable form.
# @param node_right: the argument of the arccsc function.
# @return: An expression tree that represents the arccsc function in a more suitable form.
def transform_arccsc(node_right):
    return tree.TreeNode(
        "arcsin", None, tree.TreeNode("/", tree.TreeNode("1"), node_right)
    )


# Transforms the arccot function in a more suitable form.
# @param node_right: the argument of the arccot function.
# @return: An expression tree that represents the arccot function in a more suitable form.
def transform_arccot(node_right):
    return tree.TreeNode(
        "arctan", None, tree.TreeNode("/", tree.TreeNode("1"), node_right)
    )


# Transforms the sinh function in a more suitable form.
# @param node_right: the argument of the sinh function.
# @return: An expression tree that represents the sinh function in a more suitable form.
def transform_sinh(node_right):
    return tree.TreeNode(
        "/",
        tree.TreeNode(
            "-",
            tree.TreeNode("exp", None, node_right),
            tree.TreeNode(
                "exp",
                None,
                tree.TreeNode(
                    "*",
                    tree.TreeNode("-", tree.TreeNode("0"), tree.TreeNode("1")),
                    node_right,
                ),
            ),
        ),
        tree.TreeNode("2"),
    )


# Transforms the cosh function in a more suitable form.
# @param node_right: the argument of the cosh function.
# @return: An expression tree that represents the cosh function in a more suitable form.
def transform_cosh(node_right):
    return tree.TreeNode(
        "/",
        tree.TreeNode(
            "+",
            tree.TreeNode("exp", None, node_right),
            tree.TreeNode(
                "exp",
                None,
                tree.TreeNode(
                    "*",
                    tree.TreeNode("-", tree.TreeNode("0"), tree.TreeNode("1")),
                    node_right,
                ),
            ),
        ),
        tree.TreeNode("2"),
    )


# Transforms the tanh function in a more suitable form.
# @param node_right: the argument of the tanh function.
# @return: An expression tree that represents the tanh function in a more suitable form.
def transform_tanh(node_right):
    return tree.TreeNode(
        "/",
        tree.TreeNode(
            "-",
            tree.TreeNode("exp", None, node_right),
            tree.TreeNode(
                "exp",
                None,
                tree.TreeNode("-", tree.TreeNode("0"), node_right),
            ),
        ),
        tree.TreeNode(
            "+",
            tree.TreeNode("exp", None, node_right),
            tree.TreeNode(
                "exp",
                None,
                tree.TreeNode("-", tree.TreeNode("0"), node_right),
            ),
        ),
    )


# Transforms the sech function in a more suitable form.
# @param node_right: the argument of the sech function.
# @return: An expression tree that represents the sech function in a more suitable form.
def transform_sech(node_right):
    return tree.TreeNode(
        "/",
        tree.TreeNode("2"),
        tree.TreeNode(
            "+",
            tree.TreeNode("exp", None, node_right),
            tree.TreeNode(
                "exp", None, tree.TreeNode("-", tree.TreeNode("0"), node_right)
            ),
        ),
    )


# Transforms the csch function in a more suitable form.
# @param node_right: the argument of the csch function.
# @return: An expression tree that represents the csch function in a more suitable form.
def transform_csch(node_right):
    return tree.TreeNode(
        "/",
        tree.TreeNode("2"),
        tree.TreeNode(
            "-",
            tree.TreeNode("exp", None, node_right),
            tree.TreeNode(
                "exp", None, tree.TreeNode("-", tree.TreeNode("0"), node_right)
            ),
        ),
    )


# Transforms the coth function in a more suitable form.
# @param node_right: the argument of the coth function.
# @return: An expression tree that represents the coth function in a more suitable form.
def transform_coth(node_right):
    return tree.TreeNode(
        "/",
        tree.TreeNode(
            "+",
            tree.TreeNode("exp", None, node_right),
            tree.TreeNode(
                "exp",
                None,
                tree.TreeNode("-", tree.TreeNode("0"), node_right),
            ),
        ),
        tree.TreeNode(
            "-",
            tree.TreeNode("exp", None, node_right),
            tree.TreeNode(
                "exp",
                None,
                tree.TreeNode("-", tree.TreeNode("0"), node_right),
            ),
        ),
    )


# Transforms the arcsinh function in a more suitable form.
# @param node_right: the argument of the arcsinh function.
# @return: An expression tree that represents the arcsinh function in a more suitable form.
def transform_arcsinh(node_right):
    return tree.TreeNode(
        "ln",
        None,
        tree.TreeNode(
            "+",
            node_right,
            tree.TreeNode(
                "sqrt",
                None,
                tree.TreeNode(
                    "+",
                    tree.TreeNode("^", node_right, tree.TreeNode("2")),
                    tree.TreeNode("1"),
                ),
            ),
        ),
    )


# Transforms the arccosh function in a more suitable form.
# @param node_right: the argument of the arccosh function.
# @return: An expression tree that represents the arccosh function in a more suitable form.
def transform_arccosh(node_right):
    return tree.TreeNode(
        "ln",
        None,
        tree.TreeNode(
            "+",
            node_right,
            tree.TreeNode(
                "sqrt",
                None,
                tree.TreeNode(
                    "-",
                    tree.TreeNode("^", node_right, tree.TreeNode("2")),
                    tree.TreeNode("1"),
                ),
            ),
        ),
    )


# Transforms the arctanh function in a more suitable form.
# @param node_right: the argument of the arctanh function.
# @return: An expression tree that represents the arctanh function in a more suitable form.
def transform_arctanh(node_right):
    return tree.TreeNode(
        "*",
        tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("2")),
        tree.TreeNode(
            "ln",
            None,
            tree.TreeNode(
                "/",
                tree.TreeNode("+", tree.TreeNode("1"), node_right),
                tree.TreeNode("-", tree.TreeNode("1"), node_right),
            ),
        ),
    )


# Transforms the arcsech function in a more suitable form.
# @param node_right: the argument of the arcsech function.
# @return: An expression tree that represents the arcsech function in a more suitable form.
def transform_arcsech(node_right):
    return tree.TreeNode(
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
                        tree.TreeNode("^", node_right, tree.TreeNode("2")),
                    ),
                ),
            ),
            node_right,
        ),
    )


# Transforms the arccsch function in a more suitable form.
# @param node_right: the argument of the arccsch function.
# @return: An expression tree that represents the arccsch function in a more suitable form.
def transform_arccsch(node_right):
    return tree.TreeNode(
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
                        tree.TreeNode("^", node_right, tree.TreeNode("2")),
                    ),
                ),
            ),
            node_right,
        ),
    )


# Transforms the arccoth function in a more suitable form.
# @param node_right: the argument of the arccoth function.
# @return: An expression tree that represents the arccoth function in a more suitable form.
def transform_arccoth(node_right):
    return tree.TreeNode(
        "*",
        tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("2")),
        tree.TreeNode(
            "ln",
            None,
            tree.TreeNode(
                "/",
                tree.TreeNode("+", node_right, tree.TreeNode("1"), ),
                tree.TreeNode("-",  node_right, tree.TreeNode("1"),),
            ),
        ),
    )
