from typing import List, Union
from CalculatorErrors import CalculatorSyntaxError

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
            tokens.append(str(-to_number(p[1:])))
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


def to_number(token: str) -> Number:
    """Convert token to int or float."""
    if '.' in token or 'e' in token or 'E' in token:
        number = float(token)
        if number.is_integer():
            return int(number)
        return number
    else:
        return int(token)
