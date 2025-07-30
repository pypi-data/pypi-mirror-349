from typing import Dict, Callable, List

def humanize_tool_descriptions(tools: Dict[str, Callable]) -> List[str]:
    """
    Humanize tool descriptions by converting them to a list of strings.
    """
    tool_descriptions = "\n".join(
            "- {name}: {description}".format(
                name=name,
                description=tool.__tool_description__.split('\n')[0]
        )
        for name, tool in tools.items()
    )
    return tool_descriptions