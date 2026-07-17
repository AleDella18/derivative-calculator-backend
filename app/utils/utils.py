import os
from jose import jwt
from sympy import sympify, simplify
import re


# Checks whether the substring starting at the given index corresponds to a function.
# @param i: The current index in the input string.
# @param tokens: A string containing an expression.
# @return: True if a function begins at index i and the length of the function token, False and 0 otherwise.
def is_function(i, tokens):
    n = len(tokens)
    functions = [
        "ln",
        "exp",
        "sqrt",
        "sinh",
        "cosh",
        "tanh",
        "sech",
        "csch",
        "coth",
        "arcsinh",
        "arccosh",
        "arctanh",
        "arcsech",
        "arccsch",
        "arccoth",
        "cos",
        "sin",
        "tan",
        "arccos",
        "arcsin",
        "arctan",
        "sec",
        "csc",
        "cot",
        "arcsec",
        "arccsc",
        "arccot",
    ]
    for f in functions:
        l = len(f)
        if i + l <= n and tokens[i : i + l] == f:
            return [True, l]
    return [False, 0]


# Checks whether the given value is an operator.
# @param value: The value to check. It can be an operator, a function, a differentiation variable, or a constant.
# @return: True if the value is an operator, False otherwise.
def is_operator(value):
    operators = {"*", "/", "+", "-", "^"}
    if value in operators:
        return True
    return False


# Computes the length of the number starting in position i in the tokens.
# @param i: The current index in the input string.
# @param tokens: A string containing an expression.
# @return: the length of the number starting in position i in the tokens.
def compute_number(i, tokens):
    digits = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."}
    len_tokens = len(tokens)
    length = i
    while length < len_tokens and tokens[length] in digits:
        length += 1
    return length


# Convert a string in its corresponding expression.
# @param expr_str: A string containing an expression.
# @return: The expression of the given string.
def string_to_expression(expr_str):
    expr = sympify(expr_str)
    result = "(" + str(simplify(expr)) + ")"
    return result


# Checks whether the substring starting at the given index corresponds to a variable.
# @param i: The current index in the input string.
# @param tokens: A string containing an expression.
# @return: True if a variable begins at index i and the length of the variable token, False and 0 otherwise.
def is_variable(i, tokens):
    digits = {
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    }
    length = 0
    if tokens[i] in digits:
        length = compute_number(i, tokens) - i - 1
        return [True, length]

    elif tokens[i].isalpha():
        return [True, length]

    else:
        return [False, 0]


SECRET_KEY = os.getenv("SECRET_KEY", "BrUJTuTS28idUj5sfo2370BkUREjY3M2CJjp01UVrNm")
ALGORITHM = "HS256"


# Decodes a JWT token and extracts the username from its payload.
# @param token: A JSON Web Token string.
# @return: The username stored in the "sub" field of the token payload.
def jwt_decoder(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    return username


# Checks whether a password is valid according to the security requirements.
# A valid password must be at least 8 characters long and contain at least
# one uppercase letter, one lowercase letter, one digit, and one symbol.
# @param password: The password string to validate.
# @return: True if the password satisfies all the requirements, False otherwise.
def is_valid_password(password):
    if len(password) < 8:
        return False

    has_uppercase = bool(re.search(r"[A-Z]", password))
    has_lowercase = bool(re.search(r"[a-z]", password))
    has_number = bool(re.search(r"[0-9]", password))
    has_symbol = bool(re.search(r"[^A-Za-z0-9]", password))

    return has_uppercase and has_lowercase and has_number and has_symbol
