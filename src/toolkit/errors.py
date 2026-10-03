class EmptyExpressionError(ValueError): # обрабатывает пустое выражение
    pass


class InvalidSymbolError(ValueError): # обрабатывает неверный символ
    pass


class MissingOperandError(ValueError): # пропущенный операнд
    pass


class ConsecutiveOperatorsError(ValueError): # обрабатывает некорректные последовательные операторы
    pass


class UnknownUnitError(ValueError): # обрабатывает неизвестную единицу измерения
    pass


class IncompatibleUnitsError(ValueError): # обрабатывает несовместимые единицы измерения
    pass


class InvalidValueError(ValueError): # некорректное число
    pass


class UnacceptableTemperatureError(ValueError): # некорректная температура
    pass