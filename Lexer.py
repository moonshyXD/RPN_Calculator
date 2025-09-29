from typing import List, Union, Optional
from CalculatorErrors import CalculatorSyntaxError

Number = Union[int, float]

def tokenize(expression: str) -> List[str]:
    """
    Tokenize an RPN expression line.
    Assumes tokens are separated by whitespace.
    Keeps parentheses tokens '(' and ')'.
    Numbers may have leading + or -.
    """
    expression = expression.strip().split()
    tokens = []
    for p in expression:
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

def parse_number(token: str) -> Optional[Number]:
    """Try to parse token into number. Return None if not a number."""
    try:
        if "." in token or "e" in token or "E" in token:
            num = float(token)
            return int(num) if num.is_integer() else num
        return int(token)
    except ValueError:
        return None


def to_number(token: str) -> Number:
    """Convert token to number or raise error."""
    value = parse_number(token)
    if value is None:
        raise CalculatorSyntaxError(f"Invalid number: {token}")
    return value


def is_number(token: str) -> bool:
    return parse_number(token) is not None
