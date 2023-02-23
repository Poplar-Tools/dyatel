from __future__ import annotations

from copy import copy
from typing import Any, Union

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.base.element import Element
from dyatel.mixins.driver_mixin import get_driver_wrapper_from_object
from dyatel.mixins.internal_utils import get_child_elements_with_names
from dyatel.mixins.element_mixin import shadow_class, repr_builder, all_mid_level_elements
from dyatel.mixins.previous_object_mixin import PreviousObjectDriver


class Group(Element):
    """ Group of elements. Should be defined as class """

    _is_group = True

    def __new__(cls, *args, **kwargs):
        return shadow_class(cls)

    def __repr__(self):
        return repr_builder(self, Group)

    def __init__(
            self,
            locator: str = '',
            locator_type: str = '',
            name: str = '',
            parent: Union[Any, False] = None,
            wait: bool = None,
            driver_wrapper: Union[DriverWrapper, Any] = None,
            **kwargs
    ):
        """
        Initializing of group based on current driver

        :param locator: anchor locator of group. Can be defined without locator_type
        :param locator_type: Selenium only: specific locator type
        :param name: name of group (will be attached to logs)
        :param parent: parent of element. Can be Group or Page objects of False for skip
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        :param driver_wrapper: set custom driver for group and group elements
        :param kwargs:
          - desktop: str = locator that will be used for desktop platform
          - mobile: str = locator that will be used for all mobile platforms
          - ios: str = locator that will be used for ios platform
          - android: str = locator that will be used for android platform
        """
        self._init_locals = locals()
        self._driver_instance = get_driver_wrapper_from_object(driver_wrapper)
        self._modify_children()

        super().__init__(
            locator=locator,
            locator_type=locator_type,
            name=name,
            parent=parent,
            wait=wait
        )

    def _modify_children(self):
        """
        Set parent and custom driver for Group class variables, if their instance is Element class
        Will be called automatically after __init__ by metaclass `AfterInitMeta`
        """
        for name, value in get_child_elements_with_names(self, all_mid_level_elements()).items():
            setattr(self, name, copy(value))
            value = getattr(self, name)
            if value.parent is None:
                value.parent = self
            else:
                setattr(value, 'parent', copy(value.parent))

    def _modify_object(self):
        PreviousObjectDriver().set_driver_from_previous_object_for_page_or_group(self, 6)
