from app.models import tree
from app.utils.utils import is_operator, is_function, string_to_expression


# Simplifies an expression tree as much as possible.
# @param derivative: The expression tree of certain expression.
# @return: A string representing the expression in its most simplified form,
# or "Division by zero is not allowed" if a 0 denominator is find.
def simplifier(derivative):
    stack = tree.level_order_traversal(derivative)
    functions = {"ln", "sqrt", "exp", "cos", "sin", "-sin", "tan", "arcsin", "arccos", "arctan"}
    root = stack[0]
    while stack:
        node = stack.pop()

        if is_operator(node.value):

            node.value = "(" + node.left.value + node.value + node.right.value + ")"
        

        elif node.value in functions:
            node.value = node.value + "(" + node.right.value + ")"
        

    root.value = string_to_expression(root.value)
    return root.value[1:-1]
