import re

from mops.base.group import Group
from mops.mixins.objects.locator import Locator


class SomeGroup(Group):
    def __init__(self):
        super().__init__(Locator('xpath=Group'), name='Group tests_element_repr.py')

def test_driver_wrapper_repr_playwright(mocked_play_driver):
    pattern = r"MockedDriverWrapper\(1_driver=<MagicMock id='.*'>\) at 0x.*, platform=desktop"
    assert re.search(pattern, repr(mocked_play_driver)), repr(mocked_play_driver)

def test_driver_wrapper_repr_selenium(mocked_selenium_driver):
    pattern = (r'MockedDriverWrapper\(1_driver=<selenium.webdriver.remote.webdriver.WebDriver '
               r'\(session="None"\)>\) at 0x.*, platform=desktop')
    assert re.search(pattern, repr(mocked_selenium_driver)), repr(mocked_selenium_driver)

def test_driver_wrapper_repr_ios(mocked_ios_driver):
    pattern = (r'MockedDriverWrapper\(1_driver=<appium.webdriver.webdriver.WebDriver '
               r'\(session="None"\)>\) at 0x.*, platform=ios')
    assert re.search(pattern, repr(mocked_ios_driver)), repr(mocked_ios_driver)

def test_driver_wrapper_repr_android(mocked_android_driver):
    pattern = (r'MockedDriverWrapper\(1_driver=<appium.webdriver.webdriver.WebDriver '
               r'\(session="None"\)>\) at 0x.*, platform=android')
    assert re.search(pattern, repr(mocked_android_driver)), repr(mocked_android_driver)

def test_driver_wrapper_repr_multiple_driver(
        mocked_play_driver,
        mocked_selenium_driver,
        mocked_ios_driver,
        mocked_android_driver
):
    pattern = r"MockedDriverWrapper\(1_driver=<MagicMock id='.*'>\) at 0x.*, platform=desktop"
    assert re.search(pattern, repr(mocked_play_driver)), repr(mocked_play_driver)

    pattern = (r'ShadowDriverWrapper\(2_driver=<selenium.webdriver.remote.webdriver.WebDriver '
               r'\(session="None"\)>\) at 0x.*, platform=desktop')
    assert re.search(pattern, repr(mocked_selenium_driver)), repr(mocked_selenium_driver)

    pattern = (r'ShadowDriverWrapper\(3_driver=<appium.webdriver.webdriver.WebDriver '
               r'\(session="None"\)>\) at 0x.*, platform=ios')
    assert re.search(pattern, repr(mocked_ios_driver)), repr(mocked_ios_driver)

    pattern = (r'ShadowDriverWrapper\(4_driver=<appium.webdriver.webdriver.WebDriver '
               r'\(session="None"\)>\) at 0x.*, platform=android')
    assert re.search(pattern, repr(mocked_android_driver)), repr(mocked_android_driver)

