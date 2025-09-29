from typing import List, Union
from Operations import OPERATORS
from CalculatorErrors import CalculatorSyntaxError
import Lexer

Number = Union[int, float]


def push_value(stack: List[List[Number]], value: Number) -> None:
    stack[-1].append(value)


def pop_value(stack: List[List[Number]]) -> Number:
    if not stack[-1]:
        raise CalculatorSyntaxError("Not enough values for operation")
    return stack[-1].pop()


def calculate(tokens: List[str]) -> Number:
    """Evaluate tokens in RPN. Supports parentheses as grouping."""
    expressions_stack: List[List[Number]] = [[]]

    for token in tokens:
        if token == "(":
            expressions_stack.append([])
            continue
        if token == ")":
            if len(expressions_stack) == 1:
                raise CalculatorSyntaxError("Closed parenthesis without open")
            inner = expressions_stack.pop()
            if len(inner) != 1:
                raise CalculatorSyntaxError("Parenthesis content must reduce to single value")
            push_value(expressions_stack, inner[0])
            continue

        if Lexer.is_number(token):
            value = Lexer.to_number(token)
            push_value(expressions_stack, value)
            continue

        if token not in OPERATORS:
            raise CalculatorSyntaxError(f"Unknown token: {token}")

        if len(expressions_stack[-1]) < 2:
            raise CalculatorSyntaxError(f"Not enough operands for {token}")

        b = pop_value(expressions_stack)
        a = pop_value(expressions_stack)

        result = OPERATORS[token](a, b)
        push_value(expressions_stack, result)

    if len(expressions_stack) != 1:
        raise CalculatorSyntaxError("Unbalanced parentheses")

    output = expressions_stack[0]
    if len(output) != 1:
        raise CalculatorSyntaxError("Invalid RPN expression")
    return output[0]
