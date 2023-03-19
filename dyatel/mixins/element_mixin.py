from __future__ import annotations

from abc import abstractmethod
from copy import copy
from typing import List, Any, Union

from dyatel.mixins.driver_mixin import DriverMixin
from dyatel.mixins.core_mixin import (
    driver_with_index,
    get_element_info,
    set_parent_for_attr,
)


def repr_builder(instance):
    class_name = instance.__class__.__name__
    obj_id = hex(id(instance))

    try:
        driver_title = driver_with_index(instance.driver_wrapper, instance.driver)
        parent_class = instance.parent.__class__.__name__ if getattr(instance, 'parent', False) else None
        locator_holder = getattr(instance, 'anchor', instance)

        locator = f'locator="{locator_holder.locator}"'
        locator_type = f'locator_type="{locator_holder.locator_type}"'
        name = f'name="{instance.name}"'
        parent = f'parent={parent_class}'
        driver = f'{driver_title}={instance.driver}'

        base = f'{class_name}({locator}, {locator_type}, {name}, {parent}) at {obj_id}'
        additional_info = driver
        return f'{base}, {additional_info}'
    except AttributeError:
        return f'{class_name} object at {obj_id}'


class ElementMixin(DriverMixin):
    """ Mixin for PlayElement and CoreElement """

    @property
    @abstractmethod
    def all_elements(self):
        raise NotImplementedError('all_elements method is not implemented for current class')

    @abstractmethod
    def wait_enabled(self, *args, **kwargs):
        raise NotImplementedError('wait_enabled method is not implemented for current class')

    @abstractmethod
    def wait_element_without_error(self, *args, **kwargs):
        raise NotImplementedError('wait_element_without_error method is not implemented for current class')

    def get_element_info(self, element: Any = None) -> str:
        """
        Get full loging data depends on parent element

        :param element: element to collect log data
        :return: log string
        """
        element = element if element else self
        return get_element_info(element)

    def _get_all_elements(self, sources: Union[tuple, list], instance_class: type) -> List[Any]:
        """
        Get all wrapped elements from sources

        :param sources: list of elements: `all_elements` from selenium or `element_handles` from playwright
        :param instance_class: attribute class to looking for
        :return: list of wrapped elements
        """
        wrapped_elements = []

        for element in sources:
            wrapped_object: Any = copy(self)
            wrapped_object.element = element
            wrapped_object._wrapped = True
            set_parent_for_attr(wrapped_object, instance_class, with_copy=True)
            wrapped_elements.append(wrapped_object)

        return wrapped_elements
