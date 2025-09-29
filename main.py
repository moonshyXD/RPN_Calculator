# File: rpn_calculator_m3.py
"""
RPN calculator (M3 variant) with optional parentheses validation.

- Supports: +, -, *, /, **, //, %
- // and % only for integers
- Unary + / - are allowed as part of number tokens (e.g., -3 or +4.5)
- Parentheses may be present in input; each parentheses group must itself be a valid RPN expression that reduces to a single value:
    Examples: ( 2 ) -> OK
              ( 1 2 + ) -> OK
              ( 1 2 ) + -> INVALID (inside parentheses leaves more than one value)
- No eval/exec used.
"""

import sys, tests
from typing import List, Union
from CalculatorErrors import *
from Operations import OPERATORS

Number = Union[int, float]


def check_parentheses(tokens: List[str]) -> None:
    """Check balanced parentheses. Raises CalculatorError on problems."""
    count = 0
    for t in tokens:
        if t == "(":
            count += 1
        elif t == ")":
            count -= 1
            if count < 0:
                raise CalculatorSyntaxError("Closed parenthesis without open")
    if count != 0:
        raise CalculatorSyntaxError("Unbalanced parentheses")


def tokenize(expression: str) -> List[str]:
    """
    Tokenize an RPN expression line.
    Assumes tokens are separated by whitespace.
    Keeps parentheses tokens '(' and ')'.
    Numbers may have leading + or -.
    """
    parts = expression.strip().split()
    tokens = []
    for p in parts:
        if p == '' or p is None:
            continue
        if p in ("(", ")"):
            tokens.append(p)
            continue
        if p[0] == "~":
            tokens.append(str(-_to_number(p[1:])))
        elif p[0] == "$":
            tokens.append(p[1:])
        else:
            tokens.append(p)
    return tokens


def is_number(token: str) -> bool:
    """Return True if token is integer or float literal (with optional leading + or -)."""
    try:
        if '.' in token or 'e' in token or 'E' in token:
            float(token)
            return True
        else:
            int(token)
            return True
    except ValueError:
        if any(ch.isdigit() for ch in token):
            raise CalculatorSyntaxError(f"Invalid number: {token}")
        return False


def _to_number(token: str) -> Number:
    """Convert token to int or float."""
    if '.' in token or 'e' in token or 'E' in token:
        number = float(token)
        if number.is_integer():
            return int(number)
        return number
    else:
        return int(token)


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

        if is_number(token):
            value = _to_number(token)
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


def run():
    tests.test_calculator()
    print(
        "Welcome to RPN calculator! Enter RPN expressions, tokens separated by spaces. "
        "Parentheses allowed. Unary +-($~) must be written with number without space."
    )
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            tokens = tokenize(line)
            check_parentheses(tokens)
            result = calculate(tokens)
            print(result)
        except ValueError:
            print("inf")
        except CalculatorError as e:
            print("CalculatorError:", e)


if __name__ == "__main__":
    run()
