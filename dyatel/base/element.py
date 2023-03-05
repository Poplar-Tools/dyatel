from __future__ import annotations

import time
from typing import Any, Union, List

from playwright.sync_api import Page as PlaywrightDriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver

from dyatel.exceptions import *
from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.dyatel_play.play_element import PlayElement
from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement
from dyatel.mixins.driver_mixin import get_driver_wrapper_from_object
from dyatel.mixins.element_mixin import shadow_class, repr_builder, set_base_class
from dyatel.mixins.previous_object_mixin import PreviousObjectDriver
from dyatel.visual_comparison import VisualComparison
from dyatel.keyboard_keys import KeyboardKeys
from dyatel.mixins.core_mixin import (
    WAIT_EL,
    is_target_on_screen,
    all_mid_level_elements,
    initialize_objects,
    get_child_elements_with_names,
)


class Element(WebElement, MobileElement, PlayElement):
    """ Element object crossroad. Should be defined as Page/Group class variable """

    _object = 'element'

    def __new__(cls, *args, **kwargs):
        return shadow_class(cls)

    def __repr__(self):
        return repr_builder(self)

    def __call__(self, driver_wrapper=None):
        if self.driver or driver_wrapper:
            self.__full_init__(driver_wrapper=driver_wrapper)

        return self

    def __init__(  # noqa
            self,
            locator: str = '',
            locator_type: str = '',
            name: str = '',
            parent: Union[Any, False] = None,
            wait: bool = None,
            **kwargs
    ):
        """
        Initializing of element based on current driver
        Skip init if there are no driver, so will be initialized in Page/Group

        :param locator: locator of element. Can be defined without locator_type
        :param locator_type: Selenium only: specific locator type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be Group or other Element objects or False for skip
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        :param kwargs:
          - desktop: str = locator that will be used for desktop platform
          - mobile: str = locator that will be used for all mobile platforms
          - ios: str = locator that will be used for ios platform
          - android: str = locator that will be used for android platform
        """
        self.locator = locator
        self.locator_type = locator_type
        self.name = name if name else locator
        self.parent = parent
        self.wait = wait
        self.is_element = self._object == 'element'
        self.is_group = self._object == 'group'

        if self.parent:
            assert isinstance(self.parent, (bool, all_mid_level_elements())), \
                f'The "parent" of "{self.name}" should take an Element/Group object or False for skip. Get {self.parent}'

        # Taking from Group first if available
        self._initialized = False
        self._init_locals = getattr(self, '_init_locals', locals())
        self._driver_instance = getattr(self, '_driver_instance', DriverWrapper)

        if self.driver:
            self.__full_init__(self.driver_wrapper if self.is_group else None)

    def __full_init__(self, driver_wrapper=None):
        self._driver_instance = get_driver_wrapper_from_object(driver_wrapper)
        self._modify_object()
        self._modify_children()

        if not self._initialized:
            super(self._set_base_class(), self).__init__(
                locator=self.locator,
                locator_type=self.locator_type,
                name=self.name,
                parent=self.parent,
                wait=self.wait
            )

        self._initialized = True

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

    def wait_element_without_error(self, timeout: int = WAIT_EL, silent: bool = False) -> Element:
        """
        Wait until element visibility without error

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until presence of "{self.name}" without error exception')

        try:
            self.wait_element(timeout=timeout, silent=True)
        except TimeoutException as exception:
            if not silent:
                self.log(f'Ignored exception: "{exception.msg}"')
        return self

    def wait_element_hidden_without_error(self, timeout: int = WAIT_EL, silent: bool = False) -> Element:
        """
        Wait until element hidden without error

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until invisibility of "{self.name}" without error exception')

        try:
            self.wait_element_hidden(timeout=timeout, silent=True)
        except TimeoutException as exception:
            if not silent:
                self.log(f'Ignored exception: "{exception.msg}"')
        return self

    def is_visible(self, silent: bool = False) -> bool:
        """
        Check is current element top left corner or bottom right corner visible on current screen

        :param silent: erase log
        :return: bool
        """
        if not silent:
            self.log(f'Check visibility of "{self.name}"')

        is_visible = self.is_displayed()

        if is_visible:
            rect, window_size = self.get_rect(), self.driver_wrapper.get_inner_window_size()
            x_end, y_end = rect['x'] + rect['width'], rect['y'] + rect['height']
            is_start_visible = is_target_on_screen(x=rect['x'], y=rect['y'], possible_range=window_size)
            is_end_visible = is_target_on_screen(x=x_end, y=y_end, possible_range=window_size)
            is_visible = is_start_visible or is_end_visible

        return is_visible

    def is_fully_visible(self, silent: bool = False) -> bool:
        """
        Check is current element top left corner and bottom right corner visible on current screen

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

    def assert_screenshot(
            self,
            filename: str = '',
            test_name: str = '',
            name_suffix: str = '',
            threshold: Union[int, float] = None,
            delay: Union[int, float] = None,
            scroll: bool = False,
            remove: List[Element] = None,
            fill_background: Union[str, bool] = False
    ) -> None:
        """
        Assert given (by name) and taken screenshot equals

        :param filename: full screenshot name. Custom filename will be used if empty string given
        :param test_name: test name for custom filename. Will try to find it automatically if empty string given
        :param name_suffix: filename suffix. Good to use for same element with positive/netagative case
        :param threshold: possible threshold
        :param delay: delay before taking screenshot
        :param scroll: scroll to element before taking the screenshot
        :param remove: remove elements from screenshot
        :param fill_background: fill background with given color or black color by default
        :return: None
        """
        delay = delay if delay else VisualComparison.default_delay
        threshold = threshold if threshold else VisualComparison.default_threshold

        VisualComparison(self.driver_wrapper, self).assert_screenshot(
            filename=filename, test_name=test_name, name_suffix=name_suffix, threshold=threshold, delay=delay,
            scroll=scroll, remove=remove, fill_background=fill_background,
        )

    def _set_base_class(self, driver=None) -> Element:
        """
        Get element class in according to current driver, and set him as base class

        :return: element class
        """
        cls = None
        driver = driver if driver else self.driver
        if isinstance(driver, PlaywrightDriver):
            cls = PlayElement,
        elif isinstance(driver, AppiumDriver):
            cls = MobileElement,
        elif isinstance(driver, SeleniumDriver):
            cls = WebElement,

        # No exception due to delayed initialization
        return set_base_class(self, Element, cls)

    def _modify_children(self):
        """
        Set parent and custom driver for Group class variables, if their instance is Element class
        Will be called automatically after __init__ by metaclass `AfterInitMeta`
        """
        initialize_objects(self, get_child_elements_with_names(self, all_mid_level_elements()))

    def _modify_object(self):
        prev_object_manager = PreviousObjectDriver()
        prev_object_manager.set_driver_from_previous_object_for_element(self, 6)
        if not self._initialized and self.parent is None:
            prev_object_manager.set_parent_from_previous_object_for_element(self, 6)
