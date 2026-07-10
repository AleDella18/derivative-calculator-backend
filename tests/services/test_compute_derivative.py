from app.services.compute_derivative import compute_derivative


def test_composed_division():
    expr = "ln ([(x - 1) ^( 2 / 3) ) / ((x+1)^(4/3)))"
    diff_var = "x"
    condition, result = compute_derivative(expr, diff_var)
    assert condition
    assert result == "2*(3 - x)/(3*(x**2 - 1))"


def test_composed_product():
    expr = "sin(x)*exp(cos(x))"
    diff_var = "x"
    condition, result = compute_derivative(expr, diff_var)
    assert condition
    assert result == "(-sin(x)**2 + cos(x))*exp(cos(x))"


def test_sin_commma():
    expr = "sin(3.14159*x)"
    diff_var = "x"
    condition, result = compute_derivative(expr, diff_var)
    assert condition
    assert result == "3.14159*cos(3.14159*x)"


def test_invalid_expr():
    expr = "(x+)^(sin(x+1))"
    diff_var = "x"
    condition, result = compute_derivative(expr, diff_var)
    assert not(condition)
    assert result == "Operator in position 3 misses one argument"


def test_division_by_zero():
    expr = "1/0"
    diff_var = "x"
    condition, result = compute_derivative(expr, diff_var)
    assert not(condition)
    assert result == "Division by zero is not allowed"
