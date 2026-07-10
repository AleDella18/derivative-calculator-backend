from app.validator.validator import (
    fix_parenthesis_and_spaces,
    is_invalid_token,
    are_valid_parenthesis,
    are_redundant_parenthesis,
    is_missing_operator,
    is_missing_operator_arg,
    is_function_missing_arg,
)


# Checks if the given token is valid or not and if it is valid it preprocesses it
# @param tokens: A string containing an expression.
# @return: Specific error if the token is invalid, the preprocessed token otherwise
def token_preprocess(tokens):
    tokens = fix_parenthesis_and_spaces(tokens)
    condition, character = is_invalid_token(tokens)
    if condition:
        return [False, f"{character} is an invalid character"]

    condition, index = are_valid_parenthesis(tokens)
    if not (condition):
        return [False, f"Invalid parenthesis in position {index}"]

    condition, index = are_redundant_parenthesis(tokens)
    if condition:
        return [False, f"Redundant parenthesis in position {index}"]

    condition, index = is_missing_operator(tokens)
    if condition:
        return [False, f"Missing operator in position {index}"]

    condition, index = is_missing_operator_arg(tokens)
    if condition:
        return [False, f"Operator in position {index} misses one argument"]

    condition, index = is_function_missing_arg(tokens)
    if condition:
        return [False, f"function in position {index} is missing parenthesis"]

    return [True, tokens]
