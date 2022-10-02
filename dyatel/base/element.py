from __future__ import annotations

import time
from typing import Any, Union

from playwright.sync_api import Page as PlaywrightDriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.dyatel_play.play_element import PlayElement
from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement
from dyatel.exceptions import UnexpectedElementsCountException, UnexpectedValueException, UnexpectedTextException
from dyatel.keyboard_keys import KeyboardKeys
from dyatel.mixins.driver_mixin import PreviousObjectDriver
from dyatel.mixins.internal_utils import WAIT_EL, get_platform_locator, is_target_on_screen, driver_index


class Element(WebElement, MobileElement, PlayElement):
    """ Element object crossroad. Should be defined as Page/Group class variable """

    def __init__(self, locator: str = '', locator_type: str = '', name: str = '',
                 parent: Any = None, wait: bool = False, **kwargs):
        """
        Initializing of element based on current driver
        Skip init if there are no driver, so will be initialized in Page/Group

        :param locator: locator of element. Can be defined without locator_type
        :param locator_type: Selenium only: specific locator type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be Group or Page objects
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        :param kwargs:
          - desktop: str = locator that will be used for desktop platform
          - mobile: str = locator that will be used for all mobile platforms
          - ios: str = locator that will be used for ios platform
          - android: str = locator that will be used for android platform
        """
        self.locator = locator
        self.locator_type = locator_type
        self.name = name
        self.parent = parent
        self.wait = wait

        self._init_locals = locals() if not hasattr(self, '_init_locals') else getattr(self, '_init_locals')
        self._driver_instance = DriverWrapper

        self.element_class = self.__set_base_class()
        if self.element_class:
            super().__init__(locator=self.locator, locator_type=self.locator_type, name=self.name, parent=self.parent,
                             wait=self.wait)

    def __repr__(self, base_class=None):
        cls = self.__class__
        class_name = cls.__name__
        base_class_name = base_class if base_class else cls.__base__.__name__
        locator = f'locator="{get_platform_locator(self)}"'
        index = driver_index(self.driver_wrapper, self.driver)
        driver = index if index else 'driver'
        parent = self.parent.__class__.__name__ if self.parent else None
        return f'{class_name}({locator}, locator_type="{self.locator_type}", name="{self.name}", parent={parent}) '\
               f'at {hex(id(self))}, base={base_class_name}, {driver}={self.driver}'

    # Following methods works same for both Selenium/Appium and Playwright APIs using dyatel methods

    # Elements interaction

    def set_text(self, text, silent=False) -> Element:
        """
        Set (clear and type) text in current element

        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Set text in "{self.name}"')

        self.clear_text(silent=True).type_text(text, silent=True)
        return self

    def send_keyboard_action(self, action: Union[str, KeyboardKeys]) -> Element:
        """
        Send keyboard action to current element

        :param action: keyboard action
        :return: self
        """
        if self.driver_wrapper.playwright:
            self.click()
            self.driver.keyboard.press(action)
        else:
            self.type_text(action)

        return self

    # Elements waits

    def wait_elements_count(self, expected_count, timeout=WAIT_EL, silent=False) -> Element:
        """
        Wait until elements count will be equal to expected value

        :param: elements_count: expected elements count
        :param: timeout: wait timeout
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until elements count will be equal to "{expected_count}"')

        is_equal, actual_count = False, None
        start_time = time.time()
        while time.time() - start_time < timeout and not is_equal:
            actual_count = self.get_elements_count(silent=True)
            is_equal = actual_count == expected_count

        if not is_equal:
            msg = f'Unexpected elements count of "{self.name}". Actual: {actual_count}; Expected: {expected_count}'
            raise UnexpectedElementsCountException(msg)

        return self

    def wait_element_text(self, timeout=WAIT_EL, silent=False):
        """
        Wait non empty text in element

        :param timeout: wait timeout
        :param silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait for any text is available in "{self.name}"')

        text = None
        start_time = time.time()
        while time.time() - start_time < timeout and not text:
            text = self.text

        if not text:
            raise UnexpectedTextException(f'Text of "{self.name}" is empty')

        return self

    def wait_element_value(self, timeout=WAIT_EL, silent=False):
        """
        Wait non empty value in element

        :param timeout: wait timeout
        :param silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait for any value is available in "{self.name}"')

        value = None
        start_time = time.time()
        while time.time() - start_time < timeout and not value:
            value = self.value

        if not value:
            raise UnexpectedValueException(f'Value of "{self.name}" is empty')

        return self

    def is_visible(self, silent: bool = False) -> bool:
        """
        Check is current element visible on current screen

        :param silent: erase log
        :return: bool
        """
        if not silent:
            self.log(f'Check visibility of "{self.name}"')

        is_visible = self.is_displayed()

        if is_visible:
            rect, window_size = self.get_rect(), self.driver_wrapper.get_inner_window_size()
            is_visible = is_target_on_screen(x=rect['x'], y=rect['y'], possible_range=window_size)

        return is_visible

    def is_fully_visible(self, silent: bool = False) -> bool:
        """
        Check is current element fully visible on current screen

        :param silent: erase log
        :return: bool
        """
        if not silent:
            self.log(f'Check fully visibility of "{self.name}"')

        is_visible = self.is_displayed()

        if is_visible:
            rect, window_size = self.get_rect(), self.driver_wrapper.get_inner_window_size()
            x_end, y_end = rect['x'] + rect['width'], rect['y'] + rect['height']
            is_start_visible = is_target_on_screen(x=rect['x'], y=rect['y'], possible_range=window_size)
            is_end_visible = is_target_on_screen(x=x_end, y=y_end, possible_range=window_size)
            is_visible = is_start_visible and is_end_visible

        return is_visible

    def __set_base_class(self):
        """
        Get element class in according to current driver, and set him as base class

        :return: element class
        """
        PreviousObjectDriver().set_driver_from_previous_object_for_element(self)

        if isinstance(self.driver, PlaywrightDriver):
            Element.__bases__ = PlayElement,
            return PlayElement
        elif isinstance(self.driver, AppiumDriver):
            Element.__bases__ = MobileElement,
            return MobileElement
        elif isinstance(self.driver, SeleniumDriver):
            Element.__bases__ = WebElement,
            return WebElement

        # No exception due to delayed initialization
