from typing import List, Union
from Operations import OPERATORS
from CalculatorErrors import CalculatorSyntaxError
import Lexer

Number = Union[int, float]


def _push(stack: List[List[Number]], value: Number) -> None:
    stack[-1].append(value)


def _pop(stack: List[List[Number]]) -> Number:
    if not stack[-1]:
        raise CalculatorSyntaxError("Not enough values for operation")
    return stack[-1].pop()


def _handle_parentheses(stack: List[List[Number]], token: str) -> None:
    if token == "(":
        stack.append([])
    elif token == ")":
        if len(stack) == 1:
            raise CalculatorSyntaxError("Closed parenthesis without open")
        inner = stack.pop()
        if len(inner) != 1:
            raise CalculatorSyntaxError("Parenthesis content must reduce to single value")
        _push(stack, inner[0])


def calculate(tokens: List[str]) -> Number:
    """Evaluate tokens in RPN. Supports parentheses as grouping."""
    stack: List[List[Number]] = [[]]

    for token in tokens:
        if token in ("(", ")"):
            _handle_parentheses(stack, token)
            continue

        if Lexer.is_number(token):
            _push(stack, Lexer.to_number(token))
            continue

        if token not in OPERATORS:
            raise CalculatorSyntaxError(f"Unknown token: {token}")

        if len(stack[-1]) < 2:
            raise CalculatorSyntaxError(f"Not enough operands for {token}")

        b = _pop(stack)
        a = _pop(stack)
        result = OPERATORS[token](a, b)
        _push(stack, result)

    if len(stack) != 1:
        raise CalculatorSyntaxError("Unbalanced parentheses")

    output = stack[0]
    if len(output) != 1:
        raise CalculatorSyntaxError("Invalid RPN expression")
    return output[0]
