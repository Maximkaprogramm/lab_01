from toolkit.errors import (
    ConsecutiveOperatorsError,
    EmptyExpressionError,
    InvalidSymbolError,
    MissingOperandError,
)


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

def tokenize(string: str) -> list[str]:
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

    while i < len(string):
        char = string[i]
        if char.isspace():
            i += 1
            continue
        if char.isdigit() or char == "." and current.count(".") == 0:
            current += char
            expect_number = False
        elif char in "+-" and expect_number is True:
            sg = char
            j = i + 1
            while j < len(string) and string[j].isspace():
                j += 1
            if j < len(string) and string[j] in "+-":
                rg_sg = string[j]
                if sg == rg_sg:
                    sg = "+"
                else: 
                    sg = "-"
                i = j
            if len(current) > 0:
                current += sg
            else:
                current = sg

        elif char in "+-*/%":
            if current:
                tokens.append(current)
                current = ""
            if char == "/" and (i + 1) < len(string) and string[i + 1] == "/":
                tokens.append("//")
                i += 1
            else:
                tokens.append(char)
            expect_number = True
        else:
            raise InvalidSymbolError("Invalid symbol")
        i += 1

    if current:
        tokens.append(current)
    if not tokens:
        raise EmptyExpressionError("Empty expression")
    return tokens
