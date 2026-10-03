

from toolkit.errors import (
    ConsecutiveOperatorsError,
    EmptyExpressionError,
    InvalidSymbolError,
    MissingOperandError,
)


def round_result(value: float) -> float:
    '''
    На вход подается: число (тип float);
    Округляет значение float до четырех знаков после запятой;
    Если исходное значение не равно нулю, а после округления получается ноль,
    то возвращает исходное значение;
    Возвращает: значение типа float;
    '''
    rounded = round(value, 4)
    if value != 0 and rounded == 0:
        return value

    return rounded


def validate(tokens: list[str]) -> bool:
    '''
    На вход подается: список элементов (тип list[str]);
    Проверяет возможность вычисления полученного выражения;
    Возвращает: булево значение (тип bool) - True в случае успешного завершения функции,
    иначе - вызывает определенное исключение (ошибка);  
    '''
    expect_number = True
    for token in tokens:
        if expect_number is True:
            try:
                float(token)
                expect_number = False
            except ValueError:
                raise ConsecutiveOperatorsError("Consecutive operators")
        else:
            if token in "+-/*%" or token == "//":
                expect_number = True
            else:
                raise MissingOperandError("Missing operand")
    if expect_number is True:
        raise MissingOperandError("Missing operand")
    return True


def apply_operator(left: float, right: float, operator: str) -> float:
    '''
    На вход подается: первое число (тип float), второе число (тип float), арифметический оператор (тип str); 
    Работает с положительными и отрицательными, дробными, целыми числами;
    Поддерживает операции: +, -, *, /, %, //;
    Вычисляет выражение в зависимости от оператора;
    Возвращает: десятичное число (тип float);
    '''
    if right == 0 and operator in ["%", "//", "/"]:
        raise ZeroDivisionError("ZeroDivision")
    if operator == "+":
        return left + right
    elif operator == '-':
        return left - right
    elif operator == '*':
        return left * right
    elif operator == "/":
        return left / right
    elif operator == "%":
        return left % right
    elif operator == "//":
        return left // right
    else:
        raise ValueError("InvalidSyntax")

def calculate(tokens: list[str]) -> float:
    '''
    На вход подается: список элементов (тип list[str]);
    Работает с положительными и отрицательными, дробными, целыми числами;
    Может принимать сложные длинные выражения;
    Поддерживает операции: +, -, *, /, %, //;
    Учитывает приоритет операций;
    Вычисляет выражение по переданному списку токенов;
    Возвращает: десятичное число (тип float);
    '''
    numbers = []
    operators = []

    for token in tokens:
        if token in "+-*/%" or token == "//":
            while operators and precedence(operators[-1]) >= precedence(token):
                right = numbers.pop()
                left = numbers.pop()
                operator = operators.pop()
                result = apply_operator(left, right, operator)
                numbers.append(result)
            operators.append(token)
        else:
            number = float(token)
            numbers.append(number)
    while operators:
        right = numbers.pop()
        left = numbers.pop()
        operator = operators.pop()
        result = apply_operator(left, right, operator)
        numbers.append(result)
    return numbers[0]

def precedence(operator: str) -> int:
    '''Определяет приоритет оператора и возвращает число (тип int)'''
    if operator in "+-":
        return 1
    elif operator in "*/%" or operator == "//":
        return 2

def tokenize(strings: str) -> list[str]:
    '''
    На вход подается: строка (тип str) - арифметическое выражение;
    Разбивает строку на токены: числа и операторы;
    Работает с положительными и отрицательными, дробными числами;
    Поддерживает операции: +, -, *, /, %, //;
    Возвращает: список элементов (типа list[str]);    
    '''
    tokens = []
    current = ""
    expect_number = True
    i = 0
    while i < len(strings):
        char = strings[i]
        if char.isdigit():
            current += char
            expect_number = False
        elif char == "." and "." not in current and len(current) > 0 or char in "+-" and expect_number is True:
            current += char
        elif char in "+-*/%":
            if char == "/" and (i + 1) < len(strings) and strings[i + 1] == "/":
                if current:
                    tokens.append(current)
                    current = ""
                tokens.append("//")
                expect_number = True
                i += 1
            else:
                if current:
                    tokens.append(current)
                    current = ""

                tokens.append(char)
                expect_number = True
        elif char.isspace():
            if len(current) > 0 and current not in "+-":
                tokens.append(current)
                current = ""
        else:
            raise InvalidSymbolError("Invalid symbol")
        i += 1
    if current:
        tokens.append(current)
        current = ""
    if not tokens:
        raise EmptyExpressionError("Empty expression")
    return tokens
