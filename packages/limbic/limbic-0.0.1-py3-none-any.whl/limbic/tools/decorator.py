import inspect

from functools import wraps
from typing import Callable, Any, Optional, Dict, get_type_hints


class ToolExecutionError(Exception):
    """
    Error raised when a tool fails to execute.
    """
    def __init__(self, message: str, developer_message: str):
        self.message = message
        self.developer_message = developer_message
        super().__init__(message)


def get_function_schema(func: Callable, name: str, description: str) -> Dict[str, Any]:
    """
    Generate OpenAI function schema from a function's signature.
    """
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    
    # Build parameters schema
    parameters = {
        "type": "object",
        "properties": {},
        "required": []
    }
    
    for param_name, param in signature.parameters.items():
        # Get parameter type
        param_type = type_hints.get(param_name, str)
        
        # Map Python types to JSON Schema types
        if param_type == int:
            json_type = "integer"
        elif param_type == float:
            json_type = "number"
        elif param_type == bool:
            json_type = "boolean"
        elif param_type == list:
            json_type = "array"
        elif param_type == dict:
            json_type = "object"
        else:
            json_type = "string"
        
        # Add parameter to schema
        parameters["properties"][param_name] = {
            "type": json_type,
        }
        
        # Add to required if no default value
        if param.default == inspect.Parameter.empty:
            parameters["required"].append(param_name)
    
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters
        }
    }

def tool(
    func: Optional[Callable] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Callable:
    """
    Decorator to mark a function as a tool and add error handling.
    Can be used with or without parameters.
    """
    def wrap(f: Callable) -> Callable:
        # Get tool name and description
        func_name = str(getattr(f, "__name__", None))
        tool_name = func_name if name is None else name
        tool_description = description or inspect.cleandoc(f.__doc__ or "")
        
        # Add tool metadata to function
        f.__tool_name__ = tool_name  # type: ignore
        f.__tool_description__ = tool_description  # type: ignore
        
        # Generate and add schema
        f.__tool_schema__ = get_function_schema(  # type: ignore
            func=f,
            name=tool_name,
            description=tool_description
        )
        
        # Handle both async and sync functions
        if inspect.iscoroutinefunction(f):
            @wraps(f)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    return await f(*args, **kwargs)
                except ToolExecutionError:
                    raise
                except Exception as e:
                    raise ToolExecutionError(
                        message=f"Error in execution of {tool_name}",
                        developer_message=f"Error in {func_name}: {str(e)}",
                    ) from e
        else:
            @wraps(f)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    return f(*args, **kwargs)
                except ToolExecutionError:
                    # make sure we raise the error and show the developer message
                    raise
                except Exception as e:
                    raise ToolExecutionError(
                        message=f"error in execution of {tool_name}. {str(e)}",
                        developer_message=f"Error in {func_name}: {str(e)}",
                    ) from e
                    
        return wrapper

    # Handle both @tool and @tool() syntax
    if func is not None:
        return wrap(func)
    
    return wrap



