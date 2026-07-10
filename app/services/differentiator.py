from app.models import tree
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
    derivative_of_arccos,
    derivative_of_arcsin,
    derivative_of_arctan
)
from app.utils.utils import is_operator, is_function


# Computes the derivative of the given expression tree.
# @param expression_tree: The expression tree representing the expression to differentiate.
# @param diff_var: The variable with respect to which the differentiation is performed.
# @return: The expression tree representing the derivative of the expression.
def differentiator(expression_tree, diff_var):
    stack = tree.level_order_traversal(expression_tree)
    derivatives = {}

    root = stack[0]

    while stack:
        node = stack.pop()
        value = node.value

        if not (tree.has_diff_var(node, diff_var)):
            derivatives[node] = derivative_of_costant()

        elif is_operator(value):
            if value == "+" or value == "-":
                derivatives[node] = derivative_of_plus_minus(node, derivatives)

            elif value == "*":
                derivatives[node] = derivative_of_product(node, derivatives)

            elif value == "/":
                derivatives[node] = derivative_of_division(node, derivatives)

            else:
                derivatives[node] = derivative_of_pow(node)
                if is_operator(node.left.value) or is_function(0, node.left.value)[0]:
                    derivatives[node] = tree.TreeNode(
                        "*", derivatives[node], derivatives[node.left]
                    )

        elif is_function(0, value)[0]:
            if value == "ln":
                derivatives[node] = derivative_of_ln(node)

            elif value == "exp":
                derivatives[node] = derivative_of_exp(node)

            elif value == "sqrt":
                derivatives[node] = derivative_of_sqrt(node)

            elif value == "sin":
                derivatives[node] = derivative_of_sin(node)

            elif value == "cos":
                derivatives[node] = derivative_of_cos(node)

            elif value == "tan":
                derivatives[node] = derivative_of_tan(node)
            
            elif value == "arcsin":
                derivatives[node] = derivative_of_arcsin(node)
            
            elif value == "arccos":
                derivatives[node] = derivative_of_arccos(node)
            
            else:
                derivatives[node] = derivative_of_arctan(node)

            if is_operator(node.right.value) or is_function(0, node.right.value)[0]:
                derivatives[node] = tree.TreeNode(
                    "*", derivatives[node], derivatives[node.right]
                )

        else:
            derivatives[node] = derivative_of_diffvar()

    return derivatives[root]
