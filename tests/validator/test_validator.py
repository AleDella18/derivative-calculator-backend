from app.validator.validator import (
    fix_parenthesis_and_spaces,
    is_invalid_token,
    are_valid_parenthesis,
    are_redundant_parenthesis,
    is_missing_operator,
    is_missing_operator_arg,
    is_function_missing_arg,
)


def test_fix_parenthesis_token():
    result = fix_parenthesis_and_spaces("([{a * (b + c}]) / d)")
    assert result == "(((a*(b+c)))/d)"


def test_invalids():
    result = is_invalid_token("3+(4$3)*5")
    assert result[0]
    assert result[1] == "$"


def test_complete_invalid():
    result = is_invalid_token(
        "exp(ln(sqrt(cos(sin(tan(x))))))+((2-4)/3.14)*((2-3)^5)*#4"
    )
    assert result[0]
    assert result[1] == "#"


def test_valid():
    result = is_invalid_token(
        "exp(ln(sqrt(cos(sin(tan(x))))))+((2-y)/3.14)*((a-b)^5)*z"
    )
    assert not (result[0])
    assert result[1] == ""


def test_unecessary_open_parenthesis():
    result, index = are_valid_parenthesis("(x+4)(")
    assert not (result)
    assert index == 5


def test_unacessary_closed_parenthesis():
    result, index = are_valid_parenthesis("((x+4)/(3*y))^(x-2))")
    assert not (result)
    assert index == 19


def test_multiple_invalid_parentheses():
    result, index = are_valid_parenthesis("((x+4)-3)+((3-y)^2)))")
    assert not (result)
    assert index == 20


def test_correct_parenthesis():
    result = are_valid_parenthesis("(((a*(b+c)))/d)")
    assert result


def test_redundant_parenthesis():
    result, index = are_redundant_parenthesis("(x+1)()")
    assert result
    assert index == 5


def test_redundant_complex_parenthesis():
    result, index = are_redundant_parenthesis(
        "exp(ln(sqrt(cos(sin(tan(x)())))))+((2-y)/3.14)*((a-b)^5)*z"
    )
    assert result
    assert index == 26


def test_missing_simple_operator():
    result, index = is_missing_operator("((2*x)+(4^3))/3x)")
    assert result
    assert index == 15


def test_missing_complex_closed_operator():
    result, index = is_missing_operator("x/3^(((((x*2+a-b))))))2+3")
    assert result
    assert index == 22


def test_missing_complex_open_operator():
    result, index = is_missing_operator("x/3(((((x*2+a-b))))))2+3")
    assert result
    assert index == 3


def test_correct_operators():
    result, _ = is_missing_operator(
        "exp(ln(sqrt(cos(sin(tan(x))))))+((2-y)/3.14)*((a-b)^5)*z"
    )
    assert not (result)


def test_missing_arg_simple_right():
    result, index = is_missing_operator_arg("(a*(b+))/d)")
    assert result
    assert index == 6


def test_missing_arg_complex_left():
    result, index = is_missing_operator_arg("(2+3)-(((*2)))")
    assert result
    assert index == 9


def test_missing_arg_begin():
    result, index = is_missing_operator_arg("*2+4-((x^2)*57+2)")
    assert result
    assert index == 0


def test_minus_begin():
    result, _ = is_missing_operator_arg("-1+2^3")
    assert not (result)


def test_plus_begin():
    result, _ = is_missing_operator_arg(
        "+1+exp(ln(sqrt(cos(sin(tan(x))))))+((2-y)/3.14)*((a-b)^5)*z"
    )
    assert not (result)


def test_operator_end():
    result, index = is_missing_operator_arg("+1*")
    assert result
    assert index == 2


def test_missing_arg_end():
    result, index = is_missing_operator_arg("2/((()))")
    assert result
    assert index == 5


def test_correct_args():
    result, _ = is_missing_operator_arg("((2+4)/1)+(3*((3)^(2/3))")
    assert not (result)


def test_incorrect_function_arg():
    result, index = is_function_missing_arg("3+4/sin3+x)")
    assert result
    assert index == 6


def test_correct_function_arg():
    result, _ = is_function_missing_arg("3+4/sin(3+x)")
    assert not (result)
