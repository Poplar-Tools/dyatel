from dataclasses import dataclass
from typing import Optional, Any, Union


@dataclass
class Locator:
    """ Represents a WEB UI element locator with platform-specific variations. """

    default: Optional[str] = None
    """
    All: The default locator for the object, used by default if no other locators are specified 
     or if no specific platform/device type is detected.
    """
    loc_type: Optional[str] = None
    """
    Selenium & Appium only: Specifies the locator type 
    (e.g., :obj:`~selenium.webdriver.common.by.By.CSS_SELECTOR`, :obj:`~selenium.webdriver.common.by.By.XPATH`, etc.).  

    If not provided, the locator type is automatically determined based on the given locator.
    """

    desktop: Optional[str] = None
    """
    All: The locator for desktop environments, typically used for browsers on desktop platforms.
    """

    mobile: Optional[str] = None
    """
    All: The locator for general mobile environments, used for mobile platforms other than iOS and Android,
     as well as for mobile resolutions of desktop browsers.
    """

    tablet: Optional[str] = None
    """
    Appium only: The locator specifically for tablet devices, useful for web and app automation on tablets. 
    The "is_tablet: True" desired_capability is required.
    """

    ios: Optional[str] = None
    """
    Appium only: The locator specifically for iOS devices, 
     allowing for targeting locators specific to iOS applications.
    """

    android: Optional[str] = None
    """
    Appium only: The locator specifically for Android devices, 
     allowing for targeting locators specific to Android applications.
    """


def take_locator_type(locator: Union[Locator, str]) -> Union[str, None]:
    """
    Safe take locator type from given object.

    :param locator: a Locator object or string containing locator.
    :return: locator type if given arg is Locator object.
    """
    return locator.loc_type if type(locator) is Locator else None
