from toolkit.errors import (
    IncompatibleUnitsError,
    InvalidTemperatureError,
    UnknownUnitError,
)


def converter(value: float, from_unit: str, to_unit: str) -> float:
    '''
    На вход подается: числовое значение (value), исходную единицу (from_unit), конечную единицу (to_unit);
    Важно: проверяет корректность указанных единиц;
    Поддерживаемые единицы измерения: g, kg, c, k, f, mm, cm, m, km.
    Проверяет их совместимость;
    Преобразовывает исходное значение;
    Возвращает: число с плавающей точкой (тип float);
    '''
    weight = ["g", "kg"]
    length = ["mm", "cm", "m", "km"]
    temperature = ["c", "k", "f"]
    all_units = temperature + length + weight
    if from_unit not in all_units or to_unit not in all_units:
        raise UnknownUnitError("Unknown unit")
    if from_unit in weight and to_unit in weight:
        issue = get_mass_coefficient(from_unit)
        result = get_mass_coefficient(to_unit)
        res_value = value * issue / result
    elif from_unit in length and to_unit in length:
        issue = get_length_coefficient(from_unit)
        result = get_length_coefficient(to_unit)
        res_value = value * issue / result
    elif from_unit in temperature and to_unit in temperature:
        res_value = convert_temperature(value, from_unit, to_unit)
    else:
        raise IncompatibleUnitsError("Incompatible units")
    return round_result(res_value)

def get_length_coefficient(unit: str) -> float:
    '''Возвращает числовой коэффициент для перевода числа из одной единицы измерения в другую (mm, cm, m, km)'''
    if unit == "mm":
        return 1e-3
    elif unit == "cm":
        return 1e-2
    elif unit == "m":
        return 1e0
    elif unit == "km":
        return 1e3
    else:
        raise UnknownUnitError("Unknown unit")

def get_mass_coefficient(unit: str) -> float:
    '''Возвращает числовой коэффициент для перевода числа из одной единицы измерения в другую (g, kg)'''
    if unit == "g": 
        return 1
    elif unit == "kg":
        return 1000
    else:
        raise UnknownUnitError("Unknown unit")

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    '''
    На вход подается: числовое значение (value), исходную единицу (from_unit), конечную единицу (to_unit);
    Поддерживаемые единицы измерения: c, k, f;
    Выполняет преобразования между единицами измерения;
    Важно: проверяет допустимые значения температур;
    Если температура выходит из допустимого диапазона - вызывается ошибка (InvalidTemperatureError);
    Если введены неподдерживаемые единицы измерения - вызывается ошибка (UnknownUnitError);
    Возвращает: число с плавающей точкой (тип float);
    '''
    if from_unit == "c" and to_unit == "f":
        if value >= -273.15:
            return value * 9 / 5 + 32
        else:
            raise InvalidTemperatureError("Invalid temperature")
    elif from_unit == "c" and to_unit == "k":
        if value >= -273.15:
            return value + 273.15
        else:
            raise InvalidTemperatureError("Invalid temperature")
    elif from_unit == 'k' and to_unit == 'c':
        if value >= 0:
            return value - 273.15
        else:
            raise InvalidTemperatureError("Invalid temperature")
    elif from_unit == "f" and to_unit == "c":
        celsius = (value - 32) * 5 / 9
        if celsius >= -273.15:
            return celsius
        else:
            raise InvalidTemperatureError("Invalid temperature")
    elif from_unit == "f" and to_unit == "k":
        kelvin = (value - 32) * 5 / 9 + 273.15
        if kelvin >= 0:
            return kelvin
        else:
            raise InvalidTemperatureError("Invalid temperature")
    elif from_unit == "k" and to_unit == "f":
        if value >= 0:
            return (value - 273.15) * 9 / 5 + 32
        else:
            raise InvalidTemperatureError("Invalid temperature")
    else:
        raise UnknownUnitError("Unknown unit")

def round_result(value: float) -> float:
    round_value = round(value, 2)

    if round_value == 0 and value != 0:
        return value
    return round_value

