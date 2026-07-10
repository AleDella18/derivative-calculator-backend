from app.validator.token_preprocess import token_preprocess


def test_preprocess_parenthesis_and_spaces():
    condition, tokens = token_preprocess("a+ [(b +c )+1]")
    assert condition
    assert tokens == "a+((b+c)+1)"


def test_preprocess_invalid():
    condition, tokens = token_preprocess("a+ [(b +c )+1+$]")
    assert not (condition)
    assert tokens == "$ is an invalid character"


def test_preprocess_invalid_parenthesis_sintax():
    condition, tokens = token_preprocess("a+ {[(b +c )+1]")
    assert not (condition)
    assert tokens == "Invalid parenthesis in position 2"


def test_preprocess_redundant_parenthesis():
    condition, tokens = token_preprocess("a* [(b /c )+1+()]")
    assert not (condition)
    assert tokens == "Redundant parenthesis in position 11"


def test_preprocess_missing_operator():
    condition, tokens = token_preprocess("a* [(b /c )+1+(x+(2*x)x)]")
    assert not (condition)
    assert tokens == "Missing operator in position 19"


def test_preprocess_missing_operator_arg():
    condition, tokens = token_preprocess("a* [(b /c )+1+(x+(2*x)+)]")
    assert not (condition)
    assert tokens == "Operator in position 20 misses one argument"


def test_preprocess_function_missing_parenthesis():
    condition, tokens = token_preprocess("a* [(b /c )+1+(x+(2*x)+sin]]")
    assert not (condition)
    assert tokens == "function in position 22 is missing parenthesis"
