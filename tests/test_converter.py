import pytest

from toolkit.converter import converter
from toolkit.errors import (
    IncompatibleUnitsError,
    UnacceptableTemperatureError,
    UnknownUnitError,
)


def test_converter_mass():
    assert converter(5000, "g", "kg") == 5
    assert converter(123, "kg", "g") == 123000
    assert converter(666, "g", "g") == 666
    assert converter(1000, "g", "kg") == 1
    assert converter(2, "kg", "g") == 2000
    assert converter(50029, "g", "kg") == 50.03
    assert converter(0.1, "g", "kg") == 0.0001
    assert converter(0.000001, "g", "kg") == pytest.approx(1e-9)

def test_converter_length():
    assert converter(200, "cm", "m") == 2
    assert converter(23, "m", "mm") == 23000
    assert converter(99, "m", "m") == 99
    assert converter(5, "km", "m") == 5000
    assert converter(2.2, "km", "m") == 2200
    assert converter(0.5, "m", "cm") == 50
    assert converter(123, "cm", "m") == 1.23 
    assert converter(2, "km", "cm") == 200000
    assert converter(11, "km", "mm") == 11000000
    assert converter(3, "cm", "mm") == 30

def test_converter_temperature():
    assert converter(0, "c", "f") == 32
    assert converter(0, "c", "k") == 273.15
    assert converter(32, "f", "c") == 0
    assert converter(32, "f", "k") == 273.15
    assert converter(273.15, "k", "c") == 0
    assert converter(273.15, "k", "f") == 32
    assert converter(100, "c", "f") == 212
    assert converter(100, "c", "k") == 373.15
    assert converter(212, "f", "c") == 100
    assert converter(373.15, "k", "c") == 100
    assert converter(36.6, "c", "f") == 97.88
    assert converter(14, "f", "c") == -10
    assert converter(-10, "c", "k") == 263.15

def test_converter__zero():
    assert converter(-273.15, "c", "k") == 0
    assert converter(0, "k", "c") == -273.15
    assert converter(0, "g", "kg") == 0
    assert converter(0, "mm", "km") == 0
    assert converter(5, "c", "f") == 41

def test_converter_unknown_unit():
    with pytest.raises(UnknownUnitError):
        converter(65, "sm", "kg")
    with pytest.raises(UnknownUnitError):
        converter(13, "kg", "ml")
    with pytest.raises(UnknownUnitError):
        converter(1000, "aa", "ko")
    
def test_converter_incompatible_units():
    with pytest.raises(IncompatibleUnitsError):
        converter(52, "kg", "m")
    with pytest.raises(IncompatibleUnitsError):
        converter(101, "mm", "kg")
    with pytest.raises(IncompatibleUnitsError):
        converter(273, "c", "km")
    with pytest.raises(IncompatibleUnitsError):
        converter(9, "mm", "k")

def test_converter_invalid_temperature():
    with pytest.raises(UnacceptableTemperatureError):
        converter(-323, "c", "k")
    with pytest.raises(UnacceptableTemperatureError):
        converter(-15, "k", "c")
    with pytest.raises(UnacceptableTemperatureError):
        converter(-7, "k", "f")
