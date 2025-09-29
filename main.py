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

import sys, Tests, Evaluate, Lexer
from CalculatorErrors import *

def run():
    Tests.test_calculator()
    print(
        "Welcome to RPN calculator! Enter RPN expressions, tokens separated by spaces. "
        "Parentheses allowed. Unary +-($~) must be written with number without space."
    )
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            tokens = Lexer.tokenize(line)
            result = Evaluate.calculate(tokens)
            print(result)
        except ValueError:
            print("inf")
        except CalculatorError as e:
            print("CalculatorError:", e)


if __name__ == "__main__":
    run()
