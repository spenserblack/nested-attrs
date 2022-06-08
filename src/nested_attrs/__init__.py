"""
This package provides some helpers for accessing and manipulating nested attributes.
"""

__all__ = ["nhasattr", "ngetattr", "nsetattr", "ndelattr"]


def _check_default(name, nargs, default):
    """
    Asserts that there is either no default or 1 default.
    """
    default_len = len(default)
    if default_len > 1:
        raise TypeError(f"{name} expects at most {nargs} arguments, got {default_len}")


def nhasattr(obj, attrs):
    """
    Returns whether the object has an attribute with the given path.

    This is done by calling ngetattr(obj, name) and catching AttributeError.
    """
    try:
        ngetattr(obj, attrs)
    except AttributeError:
        return False
    return True


def ngetattr(obj, attrs, *default):
    """
    ngetattr(target, attrs[, default]) -> value

    Get a nested attribute from the target object; ngetattr(x, 'y.z') is equivalent to
    x.y.z.

    When a default argument is given, it is returned when the attribute doesn't exist.
    Without a default, an exception will be raised.
    """
    _check_default("ngetattr", 3, default)
    attrs = attrs.split(".")
    target = obj
    for index, attr in enumerate(attrs):
        try:
            target = getattr(target, attr)
        except AttributeError as src_err:
            if default:
                return default[0]
            attribute_names = "." + ".".join(attrs[:index]) if index > 0 else ""
            raise AttributeError(
                "'{obj}{attributes}' has no attribute '{attr}'".format(
                    obj=obj.__class__.__name__, attributes=attribute_names, attr=attr
                )
            ) from src_err
    return target


def nsetattr(obj, attrs, value):
    """
    Set a nested attribute on the target object; nsetattr(x, 'y.z', None) is equivalent
    to x.y.z = None.

    When a parent attribute does not exist, an AttributeError is raised.
    """
    target, child = _get_last_parent(obj, attrs)
    setattr(target, child, value)


def ndelattr(obj, attrs):
    """
    Deletes the named attribute from the given object.

    delattr(x, 'y.z') is equivalent to ``del x.y.z''

    When a parent attribute does not exist, an AttributeError is raised.
    """
    target, child = _get_last_parent(obj, attrs)
    delattr(target, child)


def _get_last_parent(obj, attrs):
    """
    Gets the last child attribute that is also a parent, and the name of its child.

    _get_last_parent(a, 'b.c.d') is equivalent to ``(a.b.c, 'd')''
    """
    attrs = attrs.rsplit(".", 1)
    if len(attrs) > 1:
        parents, child = attrs
        target = ngetattr(obj, parents)
    else:
        target, child = obj, attrs[0]
    return target, child
