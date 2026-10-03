from decimal import Decimal

import pytest

from toolkit.calculator import calculate, round_result, tokenize, validate
from toolkit.errors import (
    ConsecutiveOperatorsError,
    EmptyExpressionError,
    InvalidSymbolError,
    MissingOperandError,
)


def test_tokenize_addition_subtraction():
    assert tokenize("10 + 3 - 2") == ["10", "+", "3", "-", "2"]
    assert tokenize("10230 - 2 + -23") == ["10230", "-", "2", "+", "-23"]

def test_tokenize_integer_division():
    assert tokenize("12 // 5") == ["12", "//", "5"]

def test_tokenize_float():
    assert tokenize("24.6 + 12.1 * 2.2") == ["24.6", "+", "12.1", "*", "2.2"]

def test_tokenize_space():
    assert tokenize("12    +  12.2  /     21  ") == ["12", "+", "12.2", "/", "21"]

def test_tokenize_emptiness():
    with pytest.raises(EmptyExpressionError):
        tokenize("")

def test_tokenize_invalid_symbol():
    with pytest.raises(InvalidSymbolError):
        tokenize("101 + 2 - zzzz")
    
def test_validate_correct_entry():
    assert validate(["21", "*", "-2"]) is True

def test_validate_several_operators_nearby():
    with pytest.raises(ConsecutiveOperatorsError):
        validate(["301", "%", "-", "1"])

def test_validate_missing_operand():
    with pytest.raises(MissingOperandError):
        validate(["10", "*"])

def test_validate_operator_at_start():
    with pytest.raises(ConsecutiveOperatorsError):
        validate(["%", "23", "+"])

def test_calculate_addition_subtraction():
    assert calculate(["12", "+", "98", "-", "10"]) == 100
    assert calculate(["20011", "-", "11", "+", "980000"]) == 1_000_000
    assert calculate(["126000000", "+", "274000000"]) == 400_000_000


def test_calculate_multiplication_division():
    assert calculate(["130", "*", "10", "*", "2"]) == 2600
    assert calculate(["999", "/", "333", "*", "70"]) == 210
    assert calculate(["525", "/", "25", "*", "64", "/", "12"]) == 112

def test_calculate_priority():
    assert calculate(["25", "-", "5", "/", "5"]) == 24
    assert calculate(["1", "+", "33", "*", "3", "/", "99"]) == 2
    assert calculate(["2", "*", "8", "/", "16", "-", "1"]) == 0

def test_calculate_integer_division():
    assert calculate(["33", "//", "8"]) == 4
    assert calculate(["12", "//", "13"]) == 0
    assert calculate(["21", "//", "5", "//", "4"]) == 1

def test_calculate_remainder_division():
    assert calculate(["3", "%", "2"]) == 1
    assert calculate(["2912121", "%", "2000000"]) == 912121
    assert calculate(["4232", "%", "200"]) == 32

def test_calculate_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate(["9", "/", "0"])
    with pytest.raises(ZeroDivisionError):
        calculate(["121", "%", "0"])
    with pytest.raises(ZeroDivisionError):
        calculate(["27", "//", "0"])
    with pytest.raises(ZeroDivisionError):
        calculate(["10", "//", "0", "%", "2"])

def test_calculate_mixed_operators():
    assert calculate(["39", "*", "-5", "+", "102", "%", "2", "-", "15"]) == -210
    assert calculate(["-9", "+", "-5", "*", "11", "%", "12", "*", "15", "-", "1"]) == -115
    assert calculate(["15", "-", "15", "*", "1100002", "%", "125", "-", "15"]) == -30
    assert calculate(["12", "+", "1754", "-", "2311", "-", "55", "+", "600"]) == 0

def test_calculate_numbers_small_decimal():
    assert round_result(calculate(["11", "/", "3"])) == Decimal("3.6667")
    assert round_result(calculate(["11", "/", "448"])) == Decimal("0.0246")
    assert round_result(calculate(["111554", "/", "448"])) == Decimal("249.0045")
    assert round_result(calculate(["0.003", "+", "0.003"])) == Decimal("0.006")
    assert round_result(calculate(["0.2", "+", "0.1"])) == Decimal("0.3")
    assert round_result(calculate(["1", "/", "3"])) == Decimal("0.3333")
    assert round_result(calculate(["-0.0082", "-", "0.0089"])) == Decimal("-0.0171")

def test_unary_sign_with_spaces():
    assert calculate(tokenize("107 +  -  92")) == Decimal(15)
    assert calculate(tokenize("128 + 92 - +7")) == Decimal(213)
    assert calculate(tokenize("0 +  -  9999")) == Decimal(-9999)
    assert calculate(tokenize("-  117")) == Decimal(-117)
    assert calculate(tokenize("-333 - -    33")) == Decimal(-300)