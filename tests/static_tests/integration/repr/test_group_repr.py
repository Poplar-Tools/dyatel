import re

from mops.base.group import Group
from mops.mixins.objects.locator import Locator


class SomeGroup(Group):
    def __init__(self, driver_wrapper = None):
        super().__init__(Locator('xpath=Group'), name='Group tests_element_repr.py', driver_wrapper=driver_wrapper)

def test_group_repr_playwright_one_driver(mocked_play_driver):
    pattern = (r'SomeGroup\(locator="xpath=Group", name="Group tests_element_repr.py", parent=None\) '
               r'at .*, 1_driver=<MagicMock id=.*>')
    assert re.search(pattern, repr(SomeGroup())), repr(SomeGroup())

def test_group_repr_selenium_one_driver(mocked_selenium_driver):
    pattern = (r'SomeGroup\(locator="xpath=Group", name="Group tests_element_repr.py", parent=None\) '
               r'at .*, 1_driver=<selenium.webdriver.remote.webdriver.WebDriver \(session="None"\)>')
    assert re.search(pattern, repr(SomeGroup())), repr(SomeGroup())

def test_group_repr_ios_one_driver(mocked_ios_driver):
    pattern = (r'SomeGroup\(locator="xpath=Group", name="Group tests_element_repr.py", parent=None\) '
               r'at .*, 1_driver=<appium.webdriver.webdriver.WebDriver \(session="None"\)>')
    assert re.search(pattern, repr(SomeGroup())), repr(SomeGroup())

def test_group_repr_android_one_driver(mocked_android_driver):
    pattern = (r'SomeGroup\(locator="xpath=Group", name="Group tests_element_repr.py", parent=None\) '
               r'at .*, 1_driver=<appium.webdriver.webdriver.WebDriver \(session="None"\)>')
    assert re.search(pattern, repr(SomeGroup())), repr(SomeGroup())

def test_group_repr_multiple_driver(
        mocked_play_driver,
        mocked_selenium_driver,
        mocked_ios_driver,
        mocked_android_driver
):
    obj_1_driver = repr(SomeGroup(driver_wrapper=mocked_play_driver))
    assert obj_1_driver.startswith('SomeGroup(locator="xpath=Group", name="Group tests_element_repr.py", parent=None) at')
    assert '1_driver=<MagicMock' in obj_1_driver

    obj_1_driver = repr(SomeGroup(driver_wrapper=mocked_selenium_driver))
    assert obj_1_driver.startswith('SomeGroup(locator="xpath=Group", name="Group tests_element_repr.py", parent=None) at')
    assert obj_1_driver.endswith('2_driver=<selenium.webdriver.remote.webdriver.WebDriver (session="None")>')

    obj_1_driver = repr(SomeGroup(driver_wrapper=mocked_ios_driver))
    assert obj_1_driver.startswith('SomeGroup(locator="xpath=Group", name="Group tests_element_repr.py", parent=None) at')
    assert obj_1_driver.endswith('3_driver=<appium.webdriver.webdriver.WebDriver (session="None")>')

    obj_1_driver = repr(SomeGroup(driver_wrapper=mocked_android_driver))
    assert obj_1_driver.startswith('SomeGroup(locator="xpath=Group", name="Group tests_element_repr.py", parent=None) at')
    assert obj_1_driver.endswith('4_driver=<appium.webdriver.webdriver.WebDriver (session="None")>')
