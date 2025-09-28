# числа и операции в стек потом доставать
# строки по буквам не разбирать, бесконечные циклы фор не делать
# не писать в столбик

import sys, string, re
from collections import deque

OPERATOR_PRIORITY = {
    '+': 1, '-': 1,
    '*': 2, '/': 2,
    '**': 3, '//': 3,
    '$': 4, '~': 4
}


def tokenize(expression: str):
    tokens = deque()
    digits_stack = deque()
    while token := getToken(expression):
        while isDigit(token) or token == '.':
            # Push digits to stack
            digits_stack.append(token)
            expression = expression[1:]
            token = getToken(expression)
        else:
            if digits_stack:
                # Push number
                number = ''.join(digits_stack)
                tokens.append(float(number))
                digits_stack = []

        if isOperation(token):
            # Check operation
            operation = token
            tokens.append(operation)
            if operation in '$*/':
                if token == '$':
                    tokens.pop()
                if token == '~':
                    tokens.append('~')
                if operation == '*' and token == '*':
                    operation += '*'
                elif operation == '/' and token == '/':
                    operation += '/'

                print("APPEND: ", operation, token)
                tokens.append(operation)
                expression = expression[1:]

        expression = expression[1:]

    return tokens


def getToken(expression: str) -> str:
    return expression[:1]


def isDigit(token: str) -> bool:
    # Check if this token is a number
    return token in string.digits


def isOperation(token: str) -> bool:
    # check if this token is operation
    return token in ['+', '-', '*', '/', '%', '//', '**', '(', ')']


def calculate(expression: deque):
    result = deque()
    operator_stack = deque()
    digits_stack = deque()
    while token := getToken(expression):
        while isDigit(token) or token == '.':
            # Push digits to stack
            digits_stack.append(token)
            expression = expression[1:]
            token = getToken(expression)
        else:
            if digits_stack:
                # Push number
                number = ''.join(digits_stack)
                result.append(float(number))
                digits_stack = []

        if isOperation(token):
            # Push operation by priority
            while operator_stack and isOperation(operator_stack[-1]) and \
                    (OPERATOR_PRIORITY[operator_stack[-1]] >= OPERATOR_PRIORITY[token]):
                result.append(operator_stack.pop())
                print("RESULT APPEND:", result[:1])

            operator_stack.append(token)
            print("STACK APPEND:", operator_stack[:1])

        if token == '(':
            # Push opening bracket
            operator_stack.append(token)

        if token == ')':
            while operator_stack and operator_stack[-1] != '(':
                result.append(operator_stack.pop())

            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()

        expression = expression[1:]

    while operator_stack:
        result.append(operator_stack.pop())
    print(result)


def run():
    for line in sys.stdin:
        tokens = tokenize(line)
        print("TOKENS:", tokens)
        calculate(tokens)


if __name__ == '__main__':
    run()
