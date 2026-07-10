from app.models import tree
from app.utils.utils import is_function, compute_number
from app.services.transformations import (
    transform_sec,
    transform_csc,
    transform_cot,
    transform_arcsec,
    transform_arccsc,
    transform_arccot,
    transform_sinh,
    transform_cosh,
    transform_tanh,
    transform_sech,
    transform_csch,
    transform_coth,
    transform_arcsinh,
    transform_arccosh,
    transform_arctanh,
    transform_arcsech,
    transform_arccsch,
    transform_arccoth,
)


# import Tree, utils
# Coverts an expression from infix notation to postfix notation.
# @param tokens: A string containing an expression in prefix notation.
# @return: The given expression in postfix notation.
def shanting_yard(tokens):
    precedence = {"^": 3, "*": 2, "/": 2, "+": 1, "-": 1}

    right_associative = {"^": True, "*": False, "/": False, "+": False, "-": False}

    op_stack = []
    result = []

    n = len(tokens)
    i = 0
    while i < n:

        condition, length = is_function(i, tokens)

        if condition:
            op_stack.append(tokens[i : i + length])
            i += length - 1

        elif tokens[i] == "(":
            op_stack.append(tokens[i])

        elif tokens[i] == ")":
            while op_stack[-1] != "(":
                result.append(op_stack.pop())
            op_stack.pop()
            if op_stack:
                condition, length = is_function(0, op_stack[-1])
                if condition:
                    result.append(op_stack.pop())

        elif tokens[i] in precedence:
            while op_stack:
                if op_stack[-1] == "(":
                    break

                elif precedence[tokens[i]] > precedence[op_stack[-1]] or (
                    right_associative[tokens[i]]
                    and precedence[tokens[i]] == precedence[op_stack[-1]]
                ):
                    break

                result.append(op_stack.pop())

            op_stack.append(tokens[i])

        else:
            j = compute_number(i, tokens)
            if j == i:
                result.append(tokens[i])
            else:
                result.append(tokens[i:j])
                i = j - 1

        i += 1

    while op_stack:
        result.append(op_stack.pop())

    return result


# Converts an expression in postfix notation into the corresponding expression tree.
# @param tokens: A string containing an expression in postfix notation.
# @param diff_var: The variable with respect to which the differentiation is performed.
# @return: The root of the expression tree representing the expression.
def build_tree(tokens, diff_var):
    operands = {"^", "*", "/", "+", "-"}
    stack = []
    for token in tokens:
        condition, _ = is_function(0, token)

        if condition:
            right = stack.pop()

            if token == "sec":
                stack.append(transform_sec(right))

            elif token == "csc":
                stack.append(transform_csc(right))

            elif token == "cot":
                stack.append(transform_cot(right))

            elif token == "arcsec":
                stack.append(transform_arcsec(right))

            elif token == "arccsc":
                stack.append(transform_arccsc(right))

            elif token == "arccot":
                stack.append(transform_arccot(right))

            elif token == "sinh":
                stack.append(transform_sinh(right))

            elif token == "cosh":
                stack.append(transform_cosh(right))

            elif token == "tanh":
                stack.append(transform_tanh(right))

            elif token == "sech":
                stack.append(transform_sech(right))

            elif token == "csch":
                stack.append(transform_csch(right))

            elif token == "coth":
                stack.append(transform_coth(right))

            elif token == "arcsinh":
                stack.append(transform_arcsinh(right))

            elif token == "arccosh":
                stack.append(transform_arccosh(right))

            elif token == "arctanh":
                stack.append(transform_arctanh(right))

            elif token == "arcsech":
                stack.append(transform_arcsech(right))

            elif token == "arccsch":
                stack.append(transform_arccsch(right))

            elif token == "arccoth":
                stack.append(transform_arccoth(right))

            else:
                stack.append(tree.TreeNode(token, None, right))

        elif token in operands:
            right = stack.pop()
            left = stack.pop()
            if token == "^" and tree.has_diff_var(right, diff_var):
                stack.append(
                    tree.TreeNode(
                        "exp",
                        None,
                        tree.TreeNode("*", right, tree.TreeNode("ln", None, left)),
                    )
                )
            else:
                stack.append(tree.TreeNode(token, left, right))

        else:
            stack.append(tree.TreeNode(token))

    root = stack.pop()
    return root
