from app.utils.utils import is_operator, is_function, is_variable


# Converts all square and curly brackets in the input string into round brackets.
# @param tokens: A string containing an expression.
# @return: A normalized string where all '[' and '{' are replaced with '(',
#          and all ']' and '}' are replaced with ')'.
def fix_parenthesis_and_spaces(tokens):
    tokens = tokens.replace(" ", "")
    tokens = tokens.replace("[", "(")
    tokens = tokens.replace("]", ")")
    tokens = tokens.replace("{", "(")
    tokens = tokens.replace("}", ")")
    return tokens


# Checks whether the given token contains any invalid characters.
# @param tokens: A string containing an expression.
# @return: (True, invalid_character) if an invalid character is found,
#          (False, "") if no invalid characters are found.
def is_invalid_token(tokens):
    digits = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."}
    for c in tokens:
        if not (c.isalpha() or is_operator(c) or c in digits or c == "(" or c == ")"):
            return [True, c]
    return [False, ""]


# Checks whether the parentheses syntax in the given token is correct.
# @param tokens: A string containing an expression.
# @return: (True,0) if the parentheses syntax is correct,
#          (False, index) otherwise.
def are_valid_parenthesis(tokens):
    len_tokens = len(tokens)
    stack = []
    for i in range(len_tokens):
        if tokens[i] == "(" or (
            tokens[i] == ")" and (stack == [] or stack[-1][1] == ")")
        ):
            stack.append([i, tokens[i]])

        elif tokens[i] == ")":
            stack.pop()

    if stack:
        return [False, stack[-1][0]]

    return [True, 0]


# Checks whether there is at least one redundant parenthesis.
# @param tokens: A string containing an expression.
# @return: (True, index) if there is a redundant parenthesis,
#          (False,0) otherwise.
def are_redundant_parenthesis(tokens):
    len_tokens = len(tokens)
    for i in range(1, len_tokens):
        if tokens[i - 1] == "(" and tokens[i] == ")":
            return [True, i - 1]
    return [False, 0]


# Checks whether the given expression has, at least, one missing operator.
# @param tokens: A string containing an expression.
# @return: (True, index) if there is at least one missing operator,
#          (False, 0) otherwise.
def is_missing_operator(tokens):
    len_tokens = len(tokens)
    i = 0
    while i < len_tokens:
        condition, length = is_function(i, tokens)
        if condition:
            i += length - 1

        else:
            condition, length = is_variable(i, tokens)
            i += length
            if condition:
                i += 1
                j = i
                while j < len_tokens and not (is_operator(tokens[j])):
                    condition, length = is_function(j, tokens)
                    if condition:
                        j += length - 1
                    else:
                        condition, _ = is_variable(j, tokens)
                        if condition:
                            if tokens[j - 1] == "(":
                                return [True, i]
                            else:
                                return [True, j]
                    j += 1
                i = j
        i += 1

    return [False, i]


# Checks whether the given token has an operator which is missing at least one argument.
# @param tokens: A string containing an expression.
# @return: (True, index) if there is an operator which is missing one argument,
#          (False,0) otherwise.
def is_missing_operator_arg(tokens):
    len_tokens = len(tokens)
    i = 0
    j = 0
    if is_operator(tokens[i]):
        if tokens[i] != "-" and tokens[i] != "+":
            return [True, 0]
        i += 1
    while i < len_tokens:
        if is_operator(tokens[i]):
            if j == 0:
                j = i
            i += 1
            while i < len_tokens and tokens[i] == "(":
                i += 1
            if i < len_tokens:
                if is_operator(tokens[i]) or tokens[i] == ")":
                    return [True, i]
                elif tokens[i] == ")":
                    return [True, i - 1]
        i += 1

    if is_operator(tokens[len_tokens - 1]):
        return [True, len_tokens - 1]

    if j == 0:
        return [False, 0]
    for i in range(j):
        condition1, _ = is_variable(i, tokens)
        condition2, _ = is_function(i, tokens)
        if condition1 or condition2:
            return [False, 0]
    return [True, j]


# Checks whether there is a function which hasn't an argument.
# @param tokens: A string containing an expression.
# @return: (True, index) if there is a function which is missing the argument,
#          (False,0) otherwise.
def is_function_missing_arg(tokens):
    len_tokens = len(tokens)
    i = 0
    while i < len_tokens:
        condition, length = is_function(i, tokens)
        if condition:
            i += length
            if i > len_tokens - 1:
                return [True, i]
            if tokens[i] != "(":
                return [True, i - 1]
        i += 1
    return [False, 0]