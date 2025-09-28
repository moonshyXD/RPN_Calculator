from tests import *


def test_calculator():
    all_tests = tests_correct + tests_zero_division + tests_type_error + \
                tests_large_power + tests_syntax_error + \
                tests_parentheses_valid + tests_parentheses_invalid

    for tokens, expected in all_tests:
        try:
            check_parentheses(deque(tokens))
            tokens_clean = deque([t for t in tokens if t not in ("(", ")")])
            result = calculate(tokens_clean)
            if isinstance(expected, type) and issubclass(expected, BaseException):
                raise AssertionError(f"Fail: {tokens} -> expected exception {expected}, got {result}")
            else:
                assert result == expected, f"Fail: {tokens} -> {result}, expected {expected}"
        except Exception as e:
            if isinstance(expected, type) and issubclass(expected, BaseException):
                assert isinstance(e, expected), f"Fail: {tokens} -> {type(e)}, expected {expected}"
            else:
                raise

    print("All tests passed!")


import sys, string, re
from collections import deque

MAX_POWER = 10 ** 6


def check_parentheses(tokens):
    count = 0
    for t in tokens:
        if t == "(":
            count += 1
        elif t == ")":
            count -= 1
            if count < 0:
                raise SyntaxError("CLOSED PARANTHES MUST BE OPEN")
    if count != 0:
        raise SyntaxError("UNBALANCED PARENTHESES")


def tokenize(expression: str):
    # Tokenize line
    tokens = deque()
    expression = expression.strip().split()
    countStartParenthesis = 0
    countEndParenthesis = 0
    for token in expression:
        if token in '()':
            pass
        elif token[0] == '~':
            token = '-' + token[1:]
            tokens.append(token)
        elif token[0] == '$':
            token = token[1:]
            tokens.append(token)
        else:
            tokens.append(token)

    if countStartParenthesis != countEndParenthesis:
        raise SyntaxError('UNBALANCED PARENTHESIS')

    return tokens


def isNumber(token: str) -> bool:
    # Check if this token is a number
    print('TOKEN: ', token)
    try:
        float(token)
        return True
    except ValueError:
        if any(element in string.digits for element in token):
            raise SyntaxError(f'INVALID NUMBER: {token}')
        return False


def isOperation(token: str) -> bool:
    # check if this token is operation
    return token in ['+', '-', '*', '/', '**', '//', '%', '(', ')', '$', '~']


def calculate(tokens: deque):
    # calculate expression
    stack = deque()
    for token in tokens:
        if isNumber(token):
            number = float(token)
            if number.is_integer():
                stack.append(int(number))
            else:
                stack.append(number)
        elif isOperation(token):
            if len(stack) < 2:
                raise SyntaxError(f"INVALID RPN EXPRESSION FOR TOKEN {token}")
            b = stack.pop()
            a = stack.pop()

            match token:
                case '+':
                    result = a + b
                case '-':
                    result = a - b
                case '*':
                    result = a * b
                case '**':
                    if abs(b) > MAX_POWER:
                        result = float('inf')
                    else:
                        result = a ** b
                case '/':
                    if b == 0:
                        raise ZeroDivisionError
                    result = a / b
                case '//':
                    if not isinstance(a, int) or not isinstance(b, int):
                        raise TypeError("// WORKS ONLY WITH INTEGERS")
                    if b == 0:
                        raise ZeroDivisionError
                    result = a // b
                case '%':
                    if not isinstance(a, int) or not isinstance(b, int):
                        raise TypeError("% WORKS ONLY WITH INTEGERS")
                    if b == 0:
                        raise ZeroDivisionError
                    result = a % b
                case ')':
                    pass
                case '(':
                    pass
                case _:
                    raise SyntaxError("UNKNOWN OPERATION")
            stack.append(result)
        else:
            raise SyntaxError(f"UNKNOWN TOKEN: {token}")
    if len(stack) != 1:
        raise SyntaxError("INVALID RPN EXPRESSION")
    return stack.pop()


def run():
    test_calculator()
    for line in sys.stdin:
        tokens = tokenize(line)
        print("LINE:", tokens)
        result = calculate(tokens)
        try:
            print("RESULT:", result)
        except ValueError:
            result = float('inf')
            print(result)


if __name__ == '__main__':
    run()
