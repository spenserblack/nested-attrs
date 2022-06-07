"""
This package provides some helpers for accessing and manipulating nested attributes.
"""

__all__ = ["ngetattr", "nsetattr"]


def _check_default(name, nargs, default):
    """
    Asserts that there is either no default or 1 default.
    """
    default_len = len(default)
    if default_len > 1:
        raise TypeError(f"{name} expects at most {nargs} arguments, got {default_len}")


def ngetattr(target, attrs, *default):
    """
    ngetattr(target, attrs[, default]) -> value

    Get a nested attribute from the target object; ngetattr(x, 'y.z') is equivalent to
    x.y.z.

    When a default argument is given, it is returned when the attribute doesn't exist.
    Without a default, an exception will be raised.
    """
    _check_default("ngetattr", 3, default)
    raise NotImplementedError()
