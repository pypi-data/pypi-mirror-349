from limbic.tools.decorator import tool

@tool
def final_answer(answer: str) -> str:
    """
    Provide the final answer to the task.

    Parameters:
    -----------
    answer: str
        The final answer to the task.

    Returns:
    --------
    str
        The final answer to the task.
    """
    return answer
