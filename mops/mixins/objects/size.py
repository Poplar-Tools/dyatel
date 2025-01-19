import typing
from dataclasses import dataclass


@dataclass
class Size:
    """
    Represents the dimensions of an object with width and height.

    :param width: The width of the object. Can be an integer, float, or None.
    :type width: int | float | None
    :param height: The height of the object. Can be an integer, float, or None.
    :type height: int | float | None
    """
    width: typing.Union[int, float, None] = None
    height: typing.Union[int, float, None] = None
