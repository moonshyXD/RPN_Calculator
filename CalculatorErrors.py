class CalculatorError(Exception):
    """Base calculator error"""
    pass


class CalculatorZeroDivisionError(CalculatorError, ZeroDivisionError):
    """Division by zero in calculator"""
    pass


class CalculatorTypeError(CalculatorError, TypeError):
    """Wrong operand types in calculator"""
    pass


class CalculatorSyntaxError(CalculatorError, SyntaxError):
    """Syntax mistake in calculator expression"""
    pass
