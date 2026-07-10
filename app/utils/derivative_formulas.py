from app.models import tree


# Computes the derivative of a constant.
# @return: A Tree whose value is 0.
def derivative_of_costant():
    return tree.TreeNode("0")


# @param node: The node for which the derivative is computed.
# @param derivatives: A map containing the derivatives of the child nodes.
# Computes the derivative of the differentiation variable.
# @return: A Tree whose value is 1.
def derivative_of_diffvar():
    return tree.TreeNode("1")


# Computes the derivative of a sum or subtraction expression.
# @param node: The node for which the derivative is computed.
# @param derivatives: A map containing the derivatives of the child nodes.
# @return: A Tree representing the derivative of the sum or subtraction expression.
def derivative_of_plus_minus(node, derivatives):
    return tree.TreeNode(node.value, derivatives[node.left], derivatives[node.right])


# Computes the derivative of a product expression.
# @param node: The node for which the derivative is computed.
# @param derivatives: A map containing the derivatives of the child nodes.
# @return: A Tree representing the derivative of the product expression.
def derivative_of_product(node, derivatives):
    left = tree.TreeNode("*", derivatives[node.left], node.right)
    right = tree.TreeNode("*", node.left, derivatives[node.right])
    return tree.TreeNode("+", left, right)


# Computes the derivative of power expression.
# @param node: The node for which the derivative is computed.
# @return: A Tree representing the derivative of the pow expression.
def derivative_of_pow(node):
    left = node.right
    right = tree.TreeNode(
        node.value, node.left, tree.TreeNode("-", node.right, tree.TreeNode("1"))
    )
    return tree.TreeNode("*", left, right)


# Computes the derivative of a division expression.
# @param node: The node for which the derivative is computed.
# @param derivatives: A map containing the derivatives of the child nodes.
# @return: A Tree representing the derivative of the division expression.
def derivative_of_division(node, derivatives):
    left = tree.TreeNode(
        "-",
        tree.TreeNode("*", derivatives[node.left], node.right),
        tree.TreeNode("*", node.left, derivatives[node.right]),
    )
    right = tree.TreeNode("^", node.right, tree.TreeNode("2"))
    return tree.TreeNode("/", left, right)


# Computes the derivative of ln function.
# @param node: The node for which the derivative is computed.
# @return: A Tree representing the derivative of the ln function.
def derivative_of_ln(node):
    return tree.TreeNode("/", tree.TreeNode("1"), node.right)


# Computes the derivative of exp function.
# @param node: The node for which the derivative is computed.
# @return: A Tree representing the derivative of the exp function.
def derivative_of_exp(node):
    return node


# Computes the derivative of the sqrt function.
# @param node: The node for which the derivative is computed.
# @return: A Tree representing the derivative of the sqrt function.
def derivative_of_sqrt(node):
    new_node = tree.TreeNode(
        "^", node.right, tree.TreeNode("/", tree.TreeNode("1"), tree.TreeNode("2"))
    )
    return derivative_of_pow(new_node)


# Computes the derivative of the sin function.
# @param node: The node for which the derivative is computed.
# @return: A Tree representing the derivative of the sin function.
def derivative_of_sin(node):
    return tree.TreeNode("cos", None, node.right)


# Computes the derivative of the cos function.
# @param node: The node for which the derivative is computed.
# @return: A Tree representing the derivative of the cos function.
def derivative_of_cos(node):
    return tree.TreeNode("-sin", None, node.right)


# Computes the derivative of the tan function.
# @param node: The node for which the derivative is computed.
# @return: A Tree representing the derivative of the tan function.
def derivative_of_tan(node):
    return tree.TreeNode(
        "/",
        tree.TreeNode("1"),
        tree.TreeNode("^", tree.TreeNode("cos", None, node.right), tree.TreeNode("2")),
    )


# Computes the derivative of the arcsin function.
# @param node: The node for which the derivative is computed.
# @return: A Tree representing the derivative of the arcsin function.
def derivative_of_arcsin(node):
    return tree.TreeNode(
        "/",
        tree.TreeNode("1"),
        tree.TreeNode(
            "sqrt",
            None,
            tree.TreeNode(
                "-",
                tree.TreeNode("1"),
                tree.TreeNode("^", node.right, tree.TreeNode("2")),
            ),
        ),
    )


# Computes the derivative of the arccos function.
# @param node: The node for which the derivative is computed.
# @return: A Tree representing the derivative of the arccos function.
def derivative_of_arccos(node):
    return tree.TreeNode(
        "/",
        tree.TreeNode("-1"),
        tree.TreeNode(
            "sqrt",
            None,
            tree.TreeNode(
                "-",
                tree.TreeNode("1"),
                tree.TreeNode("^", node.right, tree.TreeNode("2")),
            ),
        ),
    )


# Computes the derivative of the arctan function.
# @param node: The node for which the derivative is computed.
# @return: A Tree representing the derivative of the arctan function.
def derivative_of_arctan(node):
    return tree.TreeNode(
        "/",
        tree.TreeNode("1"),
        tree.TreeNode(
            "+",
            tree.TreeNode("1"),
            tree.TreeNode("^", node.right, tree.TreeNode("2")),
        ),
    )
