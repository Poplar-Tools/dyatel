from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Union

from selenium.webdriver.common.by import By

from mops.exceptions import InvalidLocatorException
from mops.mixins.objects.locator import Locator
from mops.utils.internal_utils import all_tags


XPATH_MATCH = ("/", "./", "(/")
CSS_MATCH = ("#", ".")
CSS_REGEXP = r"[#.\[\]=]"


def get_platform_locator(obj: Any):
    """
    Get locator for current platform from object

    :param obj: Page/Group/Element
    :return: current platform locator
    """
    locator: Union[Locator, str] = obj.locator

    if type(locator) is str or not obj.driver_wrapper:
        return locator

    mobile_fallback_locator = locator.mobile or locator.default

    if obj.driver_wrapper.is_desktop:
        locator = locator.desktop or locator.default
    if obj.driver_wrapper.is_tablet:
        locator = locator.tablet or locator.default
    elif obj.driver_wrapper.is_android:
        locator = locator.android or mobile_fallback_locator
    elif obj.driver_wrapper.is_ios:
        locator = locator.ios or mobile_fallback_locator
    elif obj.driver_wrapper.is_mobile:
        locator = mobile_fallback_locator

    if not isinstance(locator, str):
        raise InvalidLocatorException(f'Cannot extract locator for current platform for following object: {obj}')

    return locator


@dataclass
class LocatorType:
    CSS = 'css'
    XPATH = 'xpath'
    ID = 'id'
    TEXT = 'text'


def set_selenium_selector(obj: Any):
    """
    Sets selenium locator & locator type
    """
    locator = obj.locator.strip()
    obj.log_locator = locator

    # Checking the supported locators

    if locator.startswith(f"{LocatorType.XPATH}="):
        obj.locator = obj.locator.split(f"{LocatorType.XPATH}=")[-1]
        obj.locator_type = By.XPATH

    elif locator.startswith(f"{LocatorType.TEXT}="):
        locator = obj.locator.split(f"{LocatorType.TEXT}=")[-1]
        obj.locator = f'//*[contains(text(), "{locator}")]'
        obj.locator_type = By.XPATH

    elif locator.startswith(f"{LocatorType.CSS}="):
        obj.locator = obj.locator.split(f"{LocatorType.CSS}=")[-1]
        obj.locator_type = By.CSS_SELECTOR

    elif locator.startswith(f"{LocatorType.ID}="):
        locator = obj.locator.split(f"{LocatorType.ID}=")[-1]
        obj.locator = f'[{LocatorType.ID}="{locator}"]'
        obj.locator_type = By.CSS_SELECTOR

    # Checking the regular locators

    elif locator.startswith(XPATH_MATCH):
        obj.locator_type = By.XPATH
        obj.log_locator = f'{LocatorType.XPATH}={locator}'

    elif locator.startswith(CSS_MATCH) or re.search(CSS_REGEXP, locator):
        obj.locator_type = By.CSS_SELECTOR
        obj.log_locator = f'{LocatorType.CSS}={locator}'

    elif locator in all_tags or all(tag in all_tags for tag in locator.split()):
        obj.locator_type = By.CSS_SELECTOR
        obj.log_locator = f'{LocatorType.CSS}={locator}'

    elif " " in locator:
        obj.locator = f'//*[contains(text(), "{locator}")]'
        obj.locator_type = By.XPATH
        obj.log_locator = f'{LocatorType.XPATH}={locator}'

    # Default to ID if nothing else matches

    else:
        locator = obj.locator.split(f"{LocatorType.ID}=")[-1]
        obj.locator = f'[{LocatorType.ID}="{locator}"]'
        obj.locator_type = By.CSS_SELECTOR
        obj.log_locator = f'{LocatorType.ID}={locator}'


DEFAULT_MATCH = (f"{LocatorType.XPATH}=", f"{LocatorType.ID}=", f"{LocatorType.CSS}=", f"{LocatorType.TEXT}=")


def set_playwright_locator(obj: Any):
    """
    Sets playwright locator & locator type
    """
    locator = obj.locator.strip()

    # Checking the supported locators

    if locator.startswith(DEFAULT_MATCH):
        pass

    # Checking the regular locators

    elif locator.startswith(XPATH_MATCH):
        obj.locator = f"{LocatorType.XPATH}={locator}"

    elif locator.startswith(CSS_MATCH) or re.search(CSS_REGEXP, locator):
        obj.locator = f"{LocatorType.CSS}={locator}"

    elif locator in all_tags:
        obj.locator = f'{LocatorType.CSS}={locator}'

    elif " " in locator:
        obj.locator = f"{LocatorType.TEXT}={locator}"

    # Default to ID if nothing else matches

    else:
        obj.locator = f"{LocatorType.ID}={locator}"

    obj.log_locator = obj.locator
    obj.locator_type = None


def set_appium_selector(obj: Any):
    """
    Sets appium locator & locator type
    """
    locator = obj.locator.strip()

    # Mobile com.android selector

    if ':id' in locator:
        obj.locator_type = By.CSS_SELECTOR
        obj.log_locator = f'{LocatorType.ID}={locator}'
