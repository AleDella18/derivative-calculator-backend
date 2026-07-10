from app.services.parser import shanting_yard, build_tree
from app.services.differentiator import differentiator
from app.services.simplifier import simplifier
from app.validator.token_preprocess import token_preprocess
from app.validator.check_denominator import is_valid_denominator


# Computes the derivative of a given expression and simplifies it as much as possible.
# @param expr:  A string containing an expression in prefix notation.
# @param diff_var: The variable with respect to which the differentiation is performed.
# @return: A list [success, value] where:
#          - success (bool): True if the derivative was successfully computed,
#                            False if the input expression is invalid.
#          - value (str): If success is True, the simplified derivative of the expression.
#                         If success is False, an error message describing why the
#                         expression is invalid.
def compute_derivative(expr, diff_var):
    condition, expr = token_preprocess(expr)

    if condition:
        post_fix_expr = shanting_yard(expr)
        expr_tree = build_tree(post_fix_expr, diff_var)
        if not(is_valid_denominator(expr_tree)):
            return [False, "Division by zero is not allowed"]
        derivative = differentiator(expr_tree, diff_var)
        result = simplifier(derivative)
        return [True, result]

    else:
        message = expr
        return [False, message]
