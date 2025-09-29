from main import *
from collections import deque

tests_correct = [
    ("3 4 +", 7),                       # 3 + 4
    ("10 2 -", 8),                      # 10 - 2
    ("3 4 2 * +", 11),                  # 3 + 4*2
    ("5 1 2 + 4 * + 3 -", 14),          # 5 + (1+2)*4 - 3
    ("2 10 **", 1024),                  # 2 ** 10
    ("3.5 2 *", 7.0),                   # дробные числа
    ("10 3 /", 10/3),                   # деление float
    ("10 3 //", 3),                     # целочисленное деление
    ("10 3 %", 1),                      # остаток от деления
    ("3", 3),                           # одно число
    ("~3", -3),                         # число с унарным минусом
    ("$3", 3)                           # число с унарным плюсом
]

tests_zero_division = [
    ("3 0 /", ZeroDivisionError),       # деление на 0
    ("3 0 //", ZeroDivisionError),      # деление на 0
    ("3 0 %", ZeroDivisionError),       # остаток от деления на 0
]

tests_type_error = [
    ("3.5 2 //", TypeError),            # float для деления //
    ("3.5 2 %", TypeError),             # float для %
]

tests_large_power = [
    (f"2 {10**9} **", float('inf')),    # слишком большая степень
]

tests_syntax_error = [
    ("3 +", SyntaxError),               # недостаточно аргументов
    ("3 4 &", SyntaxError),             # неизвестная операция
    ("", SyntaxError),                  # пустое выражение
    ("3 4 + 5", SyntaxError),           # слишком много чисел
]

tests_parentheses_valid = [
    ("( 3 4 + )", 7),                        # скобки вокруг операции
    ("2 ( 3 4 * ) +", 14),                   # вложенные скобки в конце
    ("( 3 4 * ) 2 +", 14),                   # вложенные скобки в начале
    ("2 3 + ( 3 4 * ) 3 + +", 20),           # вложенные внутри
]

tests_parentheses_invalid = [
    ("( 3 4 +", SyntaxError),                # открыта без закрытия
    ("3 4 + )", SyntaxError),                # закрыта без открытия
    ("( 2 + 3 ) )", SyntaxError),            # лишняя закрывающая
    ("( ( 2 + 3 )", SyntaxError),            # лишняя открывающая
    (") 2 3 + (", SyntaxError),              # скобки в неправильном порядке
]

def test_calculator():
    all_tests = tests_correct + tests_zero_division + tests_type_error + \
                tests_large_power + tests_syntax_error + \
                tests_parentheses_valid + tests_parentheses_invalid

    for expression, expected in all_tests:
        try:
            tokens = tokenize(expression)
            check_parentheses(deque(tokens))
            tokens_clean = deque([t for t in tokens if t not in ("(", ")")])
            result = calculate(tokens_clean)
            if isinstance(expected, type) and issubclass(expected, BaseException):
                raise AssertionError(f"Fail: {expression} -> expected exception {expected}, got {result}")
            else:
                assert result == expected, f"Fail: {expression} -> {result}, expected {expected}"
        except Exception as e:
            if isinstance(expected, type) and issubclass(expected, BaseException):
                assert isinstance(e, expected), f"Fail: {expression} -> {type(e)}, expected {expected}"
            else:
                raise

    print("All tests passed!")
