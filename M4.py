import sys, string

OPERATOR_PRIORITY = {
    '+': 1, '-': 1,
    '*': 2, '/': 2, '//': 2, '%': 2,
    '**': 3,
}


def getToken(expression: str) -> str:
    return expression[:1]


def isDigit(element: str) -> bool:
    return element in string.digits


def isOperation(element: str) -> bool:
    return element in ['+', '*', '/', '-']


def evaluate(number1: float, number2: float, operator: str) -> float:
    print(number1, operator, number2)
    match operator:
        case '+':
            return number1 + number2
        case '*':
            return number1 * number2
        case '/':
            return number1 / number2
        case '-':
            return number1 - number2
        case _:
            raise Exception('Invalid operator')


def calculate(expression: str):
    numbers_stack = []
    operator_stack = []
    digits_stack = []
    while token := getToken(expression):
        # Number handler
        while isDigit(token) or token == '.':
            digits_stack.append(token)
            expression = expression[1:]
            token = getToken(expression)
        else:
            if digits_stack:
                number = ''.join(digits_stack)
                numbers_stack.append(float(number))
                digits_stack = []

        # Operation handler
        if isOperation(token):
            while operator_stack and (OPERATOR_PRIORITY[operator_stack[-1]] >= OPERATOR_PRIORITY[token]):
                number1 = numbers_stack.pop()
                number2 = numbers_stack.pop()
                operation = operator_stack.pop()
                numbers_stack.append(evaluate(number1, number2, operation))
            operator_stack.append(token)

        expression = expression[1:]

    print("Numbers:", numbers_stack)
    print("Operator:", operator_stack)


def run():
    for line in sys.stdin:
        calculate(line)


if __name__ == '__main__':
    run()
