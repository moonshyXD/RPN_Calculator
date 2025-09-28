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

from collections import deque
import sys
from typing import Deque, List, Union
from main import test_calculator

MAX_POWER = 10 ** 6
Number = Union[int, float]


class CalculatorError(Exception):
    """Calculator error"""
    pass


def check_parentheses(tokens: Deque[str]) -> None:
    """Check balanced parentheses. Raises CalculatorError on problems."""
    count = 0
    for t in tokens:
        if t == "(":
            count += 1
        elif t == ")":
            count -= 1
            if count < 0:
                raise CalculatorError("Closed parenthesis without open")
    if count != 0:
        raise CalculatorError("Unbalanced parentheses")


def tokenize(expression: str) -> Deque[str]:
    """
    Tokenize an RPN expression line.
    Assumes tokens are separated by whitespace.
    Keeps parentheses tokens '(' and ')'.
    Numbers may have leading + or -.
    """
    parts = expression.strip().split()
    tokens = deque()
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
            raise CalculatorError(f"Invalid number: {token}")
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


def calculate(tokens: Deque[str]) -> Number:
    """Evaluate tokens in RPN. Supports parentheses as grouping."""
    frames: List[List[Number]] = [[]]

    def push_value(value: Number):
        frames[-1].append(value)

    def pop_value() -> Number:
        if not frames[-1]:
            raise CalculatorError("Not enough values for operation")
        return frames[-1].pop()

    for token in tokens:
        if token == "(":
            frames.append([])
            continue
        if token == ")":
            if len(frames) == 1:
                raise CalculatorError("Closed parenthesis without open")
            inner = frames.pop()
            if len(inner) != 1:
                raise CalculatorError("Parenthesis content must reduce to single value")
            frames[-1].append(inner[0])
            continue

        if is_number(token):
            val = _to_number(token)
            push_value(val)
            continue

        if token not in ('+', '-', '*', '/', '**', '//', '%'):
            raise CalculatorError(f"Unknown token: {token}")

        if len(frames[-1]) < 2:
            raise CalculatorError(f"Not enough operands for {token}")

        b = pop_value()
        a = pop_value()

        try:
            if token == '+':
                res = a + b
            elif token == '-':
                res = a - b
            elif token == '*':
                res = a * b
            elif token == '**':
                if abs(b) > MAX_POWER:
                    res = float('inf')
                else:
                    res = a ** b
            elif token == '/':
                if b == 0:
                    raise CalculatorError("Float division by zero")
                res = a / b
            elif token == '//':
                if not isinstance(a, int) or not isinstance(b, int):
                    raise CalculatorError("// works only with integers")
                if b == 0:
                    raise CalculatorError("Integer division by zero")
                res = a // b
            elif token == '%':
                if not isinstance(a, int) or not isinstance(b, int):
                    raise CalculatorError("% works only with integers")
                if b == 0:
                    raise CalculatorError("Modulo division by zero")
                res = a % b
            else:
                raise CalculatorError(f"Unknown operation: {token}")
        except OverflowError:
            res = float('inf')

        push_value(res)

    if len(frames) != 1:
        raise CalculatorError("Unbalanced parentheses")

    top = frames[0]
    if len(top) != 1:
        raise CalculatorError("Invalid RPN expression")
    return top[0]


def run():
    test_calculator()
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
            check_parentheses(deque(tokens))
            result = calculate(tokens)
            result_str = str(result)
            print(len(result_str))
            print(result_str)
        except ValueError:
            print("inf")
        except CalculatorError as e:
            print("CalculatorError:", e)


if __name__ == "__main__":
    run()
