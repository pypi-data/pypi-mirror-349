import sys


def trace_module(frame, event: str, arg):
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
    sys.settrace(trace_module)


def disable_trace():
    sys.settrace(None)


if __name__ == "__main__":
    enable_trace()
