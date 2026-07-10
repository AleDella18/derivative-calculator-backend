from app.models.tree import level_order_traversal
from app.utils.utils import is_operator, is_function, string_to_expression
import copy


# Checks whether the given expression has a 0 denominator or not
# @ param expr_tree: The expression tree representing the given expression
# @return: True if the denominator is valid, False if the denominator is 0
def is_valid_denominator(expr_tree):
    new_expr_tree = copy.deepcopy(expr_tree)
    stack = level_order_traversal(new_expr_tree)

    while stack:
        node = stack.pop()

        if is_operator(node.value):

            if node.value == "/":
                if string_to_expression(node.right.value) == "(0)":
                    return False

            node.value = "(" + node.left.value + node.value + node.right.value + ")"

        elif (len(node.value) <= 4) and (
            is_function(0, node.value)[0] or is_function(1, node.value)[0]
        ):
            node.value = node.value + "(" + node.right.value + ")"

    return True
