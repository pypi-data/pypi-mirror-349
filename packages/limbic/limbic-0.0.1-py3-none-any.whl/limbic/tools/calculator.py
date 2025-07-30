from limbic.tools.decorator import tool

@tool
def calculator(x: float, y: float, operation: str) -> float:
    """
    A simple calculator tool.

    Parameters:
    -----------
    x: float
        The first number to calculate.
    y: float
        The second number to calculate.
    operation: str
        The operation to perform. Can be "add" or "multiply".

    Returns:
    --------
    float
        The result of the calculation.
    """
    if operation == 'add':
        return x + y
    elif operation == 'multiply':
        return x * y
    elif operation == 'divide':
        return x / y

    raise ValueError(f"Unknown operation: {operation}")