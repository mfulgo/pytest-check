import inspect
import os

_traceback_style = "auto"


def get_full_context(frame):
    (_, filename, line, funcname, contextlist) = frame[0:5]
    try:
        filename = os.path.relpath(filename)
    except ValueError:  # pragma: no cover
        # this is necessary if we're tracing to a different drive letter
        # such as C: to D:
        #
        # Turning off coverage for abspath, for now,
        # since that path requires testing with an odd setup.
        # But.... we'll keep looking for a way to test it. :)
        filename = os.path.abspath(filename)  # pragma: no cover
    context = contextlist[0].strip() if contextlist else ""
    return (filename, line, funcname, context)


def _build_pseudo_trace_str():
    """
    built traceback styles for better error message
    only supports no
    """
    if _traceback_style == "no":
        return ""

    skip_own_frames = 3
    pseudo_trace = []
    func = ""
    context_stack = inspect.stack()[skip_own_frames:]
    while "test_" not in func and context_stack:
        (file, line, func, context) = get_full_context(context_stack.pop(0))
        # we want to trace through user code, not 3rd party or builtin libs
        if "site-packages" in file:
            break
        # if called outside of a test, we might hit this
        if "<module>" in func:
            break
        line = f"{file}:{line} in {func}() -> {context}"
        pseudo_trace.append(line)

    return "\n".join(reversed(pseudo_trace)) + "\n"
