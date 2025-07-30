import sys
from types import FrameType
from typing import Any


def trace_module(frame: FrameType, event: str, arg: Any):
    """Trace module imports.

    Args:
        frame (FrameType): The current stack frame.
        event (str): The event type (e.g., "call", "return").
        arg (Any): Additional event-specific information.

    Returns:
        Any: The return value of the traced function or None.
    """
    code = frame.f_code
    module_name = code.co_filename
    if (
        event == "call"
        and ".pyenv" not in module_name
        and ".cache" not in module_name
        and "<" not in module_name
    ):
        print(f"Module loaded: {module_name}")
    return trace_module


def enable_trace():
    """Enable tracing of module imports."""
    sys.settrace(trace_module)


def disable_trace():
    """Disable tracing of module imports."""
    sys.settrace(None)
