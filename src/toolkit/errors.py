class EmptyExpressionError(ValueError):
    pass


class InvalidSymbolError(ValueError):
    pass


class MissingOperandError(ValueError):
    pass


class ConsecutiveOperatorsError(ValueError):
    pass


class UnknownUnitError(ValueError):
    pass


class IncompatibleUnitsError(ValueError):
    pass


class InvalidNumberError(ValueError):
    pass


class InvalidTemperatureError(ValueError):
    pass