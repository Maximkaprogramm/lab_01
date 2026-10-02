
import argparse
import sys

from toolkit.calculator import calculate, tokenize, validate
from toolkit.converter import converter
from toolkit.errors import (
    ConsecutiveOperatorsError,
    EmptyExpressionError,
    IncompatibleUnitsError,
    InvalidNumberError,
    InvalidSymbolError,
    InvalidTemperatureError,
    MissingOperandError,
    UnknownUnitError,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Калькулятор и конвертер единиц")
    subparsers = parser.add_subparsers(dest="command", required=True)
    calc_parser = subparsers.add_parser("calc", help="Вычислить арифметическое выражение")
    calc_parser.add_argument("expression", help="Арифметическое выражение")

    convert_parser = subparsers.add_parser("convert", help="Конвертировать единицы измерения")
    convert_parser.add_argument("value", help="Числовое значение")
    convert_parser.add_argument("from_unit", help="Исходная единица")
    convert_parser.add_argument("to_unit", help="Конечная единица")
    args = parser.parse_args()
     
    try:
        if args.command == "calc":
            element = args.expression
            tokens = tokenize(element)
            validate(tokens)
            results = calculate(tokens)
            print(results)

        elif args.command == "convert":
            value = float(args.value)
            from_unit = args.from_unit.lower()
            to_unit = args.to_unit.lower()
            results = converter(value, from_unit, to_unit)
            print(results)


    except EmptyExpressionError:
        print("Error: empty expression", file=sys.stderr)
        return 2

    except InvalidSymbolError:
        print("Error: invalid symbol", file=sys.stderr)
        return 2

    except MissingOperandError:
        print("Error: missing operand", file=sys.stderr)
        return 2

    except ZeroDivisionError:
        print("Error: division by zero", file=sys.stderr)
        return 2
    except ConsecutiveOperatorsError:
        print("Error: consecutive operators", file=sys.stderr)
        return 2

    except UnknownUnitError:
        print("Error: unknown unit", file=sys.stderr)
        return 2

    except InvalidNumberError:
        print("Error: invalid number", file=sys.stderr)
        return 2

    except IncompatibleUnitsError:
        print("Error: incompatible units", file=sys.stderr)
        return 2
    except InvalidTemperatureError:
        print("Error: invalid temperature", file=sys.stderr)
        return 2
    


if __name__ == "__main__":
    sys.exit(main())
