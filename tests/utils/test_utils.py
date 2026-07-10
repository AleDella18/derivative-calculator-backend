from app.utils.utils import (
    is_function,
    is_operator,
    compute_number,
    string_to_expression,
    is_variable,
    is_valid_password,
)


def test_ln():
    condition, length = is_function(4, "3*2+ln(9)")
    assert condition
    assert length == 2


def test_exp():
    condition, length = is_function(8, "3*2+3/8+exp(9)")
    assert condition
    assert length == 3


def test_sqrt():
    condition, length = is_function(6, "3*2+6-sqrt(9)+6-7")
    assert condition
    assert length == 4


def test_sin():
    condition, length = is_function(2, "3+sin(30)+6-7")
    assert condition
    assert length == 3


def test_cos():
    condition, length = is_function(4, "3+6-cos(90)+7")
    assert condition
    assert length == 3


def test_tan():
    condition, length = is_function(6, "3+6^2-tan(180)+7")
    assert condition
    assert length == 3


def test_arccos():
    condition, length = is_function(6, "x+7^2-arccos(1/2)+7")
    assert condition
    assert length == 6


def test_arcsin():
    condition, length = is_function(2, "y+arcsin(1)+7")
    assert condition
    assert length == 6


def test_arctan():
    condition, length = is_function(6, "y+2*4+arctan(0)")
    assert condition
    assert length == 6


def test_sec():
    condition, length = is_function(9, "exp(x*2)+sec(x)")
    assert condition
    assert length == 3


def test_csc():
    condition, length = is_function(8, "ln(x^2)+csc(x)")
    assert condition
    assert length == 3


def test_cot():
    condition, length = is_function(9, "exp(x*2)+cot(x)")
    assert condition
    assert length == 3


def test_arcsec():
    condition, length = is_function(9, "exp(x*2)+arcsec(x)")
    assert condition
    assert length == 6


def test_arccsc():
    condition, length = is_function(8, "ln(x^2)+arccsc(x)")
    assert condition
    assert length == 6


def test_arccot():
    condition, length = is_function(9, "exp(x*2)+arccot(x)")
    assert condition
    assert length == 6


def test_sinh():
    condition, lenght = is_function(0, "sinh(x)")
    assert condition
    assert lenght == 4


def test_cosh():
    condition, lenght = is_function(0, "cosh(x)")
    assert condition
    assert lenght == 4


def test_tanh():
    condition, lenght = is_function(0, "tanh(x)")
    assert condition
    assert lenght == 4


def test_sech():
    condition, lenght = is_function(0, "sech(x)")
    assert condition
    assert lenght == 4


def test_csch():
    condition, lenght = is_function(0, "csch(x)")
    assert condition
    assert lenght == 4


def test_coth():
    condition, lenght = is_function(0, "coth(x)")
    assert condition
    assert lenght == 4


def test_arcsinh():
    condition, lenght = is_function(0, "arcsinh(x)")
    assert condition
    assert lenght == 7


def test_arccosh():
    condition, lenght = is_function(0, "arccosh(x)")
    assert condition
    assert lenght == 7


def test_arctanh():
    condition, lenght = is_function(0, "arctanh(x)")
    assert condition
    assert lenght == 7


def test_arcsech():
    condition, lenght = is_function(0, "arcsech(x)")
    assert condition
    assert lenght == 7


def test_arccsch():
    condition, lenght = is_function(0, "arccsch(x)")
    assert condition
    assert lenght == 7


def test_arccsch():
    condition, lenght = is_function(0, "arccsch(x)")
    assert condition
    assert lenght == 7


def test_arccoth():
    condition, lenght = is_function(0, "arccoth(x)")
    assert condition
    assert lenght == 7


def test_no_function():
    condition, length = is_function(5, "3+6^2-tan(180)+7")
    assert not (condition)
    assert length == 0


def test_is_mult_an_operator():
    assert is_operator("*")


def test_is_div_an_operator():
    assert is_operator("/")


def test_is_plus_an_operator():
    assert is_operator("+")


def test_is_minus_an_operator():
    assert is_operator("-")


def test_is_power_an_operator():
    assert is_operator("^")


def test_single_number():
    result = compute_number(4, "2*x+1+4")
    assert result == 5


def test_composed_number():
    result = compute_number(0, "289.33*x+55")
    assert result == 6


def test_simplification():
    result = string_to_expression("x+0")
    assert result == "(x)"


def test_simplification_sin_cos():
    result = string_to_expression("sin(x)**2 + cos(x)**2")
    assert result == "(1)"


def test_simplification_complex_polynomial():
    result = string_to_expression("(x**3 + x**2 - x - 1)/(x**2 + 2*x + 1)")
    assert result == "(x - 1)"


def test_simplification_pow():
    result = string_to_expression("(x+2)**(1/2)")
    assert result == "(sqrt(x + 2))"


def test_numerical_varible():
    condition, length = is_variable(11, "(sin(x)+3)/33.55")
    assert condition
    assert length == 4


def test_alphabetic_variable():
    condition, length = is_variable(5, "(sin(x)+3)/33.55")
    assert condition
    assert length == 0


def test_is_not_variable():
    condition, length = is_variable(5, "ln(x)+3")
    assert not (condition)
    assert length == 0


def test_invalid_length():
    assert not (is_valid_password("1aA!"))


def test_invalid_lower():
    assert not (is_valid_password("123A!AAAA"))


def test_invalid_upper():
    assert not (is_valid_password("123a!aaaa"))


def test_invalid_number():
    assert not (is_valid_password("AAAa!aaaa"))


def test_invalid_special():
    assert not (is_valid_password("1AAabaaaa"))


def test_valid_password():
    assert is_valid_password("1aA!bbnbhab")
