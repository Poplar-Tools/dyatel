from __future__ import annotations

import sys
import inspect
from copy import copy
from typing import Any, Union

from dyatel.exceptions import UnsuitableArgumentsException


WAIT_EL = 10
WAIT_PAGE = 20

all_tags = {'h1', 'h2', 'h3', 'h4', 'h5', 'head', 'body', 'input', 'section', 'button', 'a', 'link', 'header', 'div',
            'textarea', 'svg', 'circle', 'iframe', 'label', 'tr', 'th', 'table', 'tbody', 'td', 'select', 'nav', 'li',
            'form', 'footer', 'frame', 'area', 'span'}


def get_frame(frame=1):
    """
    Get frame by given id

    :param frame: frame id, "current" by default
    :return: frame
    """
    return sys._getframe(frame)  # noqa


def initialize_objects_with_args(current_object, objects: dict):
    """
    Initializing objects with itself args/kwargs

    :param current_object: list of objects to initialize
    :param objects: list of objects to initialize
    :return: None
    """
    for name, obj in objects.items():
        if not getattr(obj, '_initialized', False):
            copied_obj = copy(obj)
            copied_obj._driver_instance = current_object._driver_instance  # noqa
            copied_obj._set_base_class()  # noqa
            copied_obj._initialized = True
            setattr(current_object, name, copied_obj)


def get_platform_locator(obj: Any):
    """
    Get locator for current platform from object

    :param obj: Page/Group/Element
    :return: current platform locator
    """
    locator, data = obj.locator, getattr(obj, '_init_locals').get('kwargs', {})

    if not data or not obj.driver_wrapper:
        return locator

    if obj.driver_wrapper.desktop:
        locator = data.get('desktop', locator)

    elif obj.driver_wrapper.mobile:
        locator = data.get('mobile', locator)
        if data.get('mobile', False) and (data.get('android', False) or data.get('ios', False)):
            raise UnsuitableArgumentsException('Dont use mobile and android/ios locators together')
        elif obj.driver_wrapper.is_ios:
            locator = data.get('ios', locator)
        elif obj.driver_wrapper.is_android:
            locator = data.get('android', locator)

    return locator


def get_timeout_in_ms(timeout: int):
    """
    Get timeout in milliseconds for playwright

    :param timeout: timeout in seconds
    :return: timeout in milliseconds
    """
    return timeout * 1000 if timeout < 1000 else timeout


def get_child_elements(obj: object, instance: Union[type, tuple]) -> list:
    """
    Return objects of this object by instance

    :returns: list of page elements and page objects
    """
    return list(get_child_elements_with_names(obj, instance).values())


def get_child_elements_with_names(obj: Any, instance: Union[type, tuple]) -> dict:
    """
    Return objects of this object by instance

    :returns: list of page elements and page objects
    """
    elements = {}

    for attribute, value in get_all_attributes_from_object(obj).items():
        if isinstance(value, instance):
            if attribute != 'parent' and '__' not in attribute:
                elements.update({attribute: value})

    return elements


def get_all_attributes_from_object(
        reference_obj: Any,
        obj_items: Any = None,
        stop_on_base: bool = False
) -> dict:
    """

    :param reference_obj:
    :param obj_items:
    :param stop_on_base:
    :return:
    """
    if not obj_items:
        obj_items = {}

    reference_class = reference_obj if inspect.isclass(reference_obj) else reference_obj.__class__

    for parent_class in reference_class.__bases__:
        str_parent_class = str(parent_class)

        if "'object'" in str_parent_class or "'type'" in str_parent_class:
            break

        if stop_on_base and 'dyatel' in str_parent_class and 'dyatel.base' not in str_parent_class:
            continue

        obj_items.update(dict(parent_class.__dict__))
        get_all_attributes_from_object(parent_class, obj_items, stop_on_base)

    obj_items.update({attr: value for attr, value in reference_class.__dict__.items() if '__' not in str(attr)})
    # obj_items.update(dict(reference_class.__dict__))
    obj_items.update(dict(reference_obj.__dict__))

    return obj_items


def is_target_on_screen(x: int, y: int, possible_range: dict):
    """
    Check is given coordinates fit into given range

    :param x: x coordinate
    :param y: y coordinate
    :param possible_range: possible range
    :return: bool
    """
    is_x_on_screen = x in range(possible_range['width'])
    is_y_on_screen = y in range(possible_range['height'])
    return is_x_on_screen and is_y_on_screen


def calculate_coordinate_to_click(element: Any, x: int = 0, y: int = 0) -> tuple:
    """
    Calculate coordinates to click for element
    Examples:
        (0, 0) -- center of the element
        (5, 0) -- 5 pixels to the right
        (-10, 0) -- 10 pixels to the left out of the element
        (0, -5) -- 5 pixels below the element

    :param element: dyatel WebElement or MobileElement
    :param x: horizontal offset relative to either left (x < 0) or right side (x > 0)
    :param y: vertical offset relative to either top (y > 0) or bottom side (y < 0)
    :return: tuple of calculated coordinates
    """
    ey, ex, ew, eh = element.get_rect().values()
    mew, meh = ew / 2, eh / 2
    emx, emy = ex + mew, ey + meh  # middle of element

    sx, sy = ([-1, 1][s > 0] for s in [x, y])
    x = emx + bool(x) * (x + mew * sx)
    y = emy + bool(y) * (y + meh * sy)

    return int(x), int(y)


def driver_with_index(driver_wrapper, driver) -> str:
    """
    Get driver index for logging

    :param driver_wrapper: driver wrapper object
    :param driver: driver object
    :return: 'index_driver' data
    """
    try:
        index = driver_wrapper.all_drivers.index(driver) + 1
    except ValueError:
        index = '?'

    return f'{index}_driver'
