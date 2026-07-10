from app.services.parser import shanting_yard


def test_multiplication_precedence():
    result = shanting_yard("1+4*2-5")
    result = "".join(result)
    assert result == "142*+5-"


def test_division_precedence():
    result = shanting_yard("1+4/2-5")
    result = "".join(result)
    assert result == "142/+5-"


def test_parenthesis_precedence():
    result = shanting_yard("(((a*(b+c)))/d)")
    result = "".join(result)
    assert result == "abc+*d/"


def test_token_preprocess():
    result = shanting_yard("(((a*(b+c)))/d)")
    result = "".join(result)
    assert result == "abc+*d/"


def test_right_associative():
    result = shanting_yard("2^3^2")
    result = "".join(result)
    assert result == "232^^"


def test_completed():
    result = shanting_yard("(((a*(b+c)))/d)+3^5+2^4^6")
    result = "".join(result)
    assert result == "abc+*d/35^+246^^+"


def test_ln():
    result = shanting_yard("3*(4-3)+(2*ln(x))")
    result = "".join(result)
    assert result == "343-*2xln*+"


def test_exp():
    result = shanting_yard("(((a*(b+exp(x))))/d)")
    result = "".join(result)
    assert result == "abxexp+*d/"


def test_sqrt():
    result = shanting_yard("1+4/sqrt(x+2)-5")
    result = "".join(result)
    assert result == "14x2+sqrt/+5-"


def test_trigonometrics():
    result = shanting_yard("(((a*(cos(x+2)+tan(3*x))))/tan(x))+3^5+2^4^6")
    result = "".join(result)
    assert result == "ax2+cos3x*tan+*xtan/35^+246^^+"


def test_inverse_trigonometrics():
    result = shanting_yard("2*x+(arccos(x+1)/arctan(2+x))*arcsin(exp(2))")
    result = "".join(result)
    assert result == "2x*x1+arccos2x+arctan/2exparcsin*+"


def test_composed():
    result = shanting_yard("cos(exp(2*x+sqrt(x*exp(2+3*x+4))))")
    result = "".join(result)
    assert result == "2x*x23x*+4+exp*sqrt+expcos"


def test_comma():
    result = shanting_yard("sin(3.14159*x)")
    result = "".join(result)
    assert result == "3.14159x*sin"
