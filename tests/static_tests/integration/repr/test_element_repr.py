import re

from mops.base.element import Element
from mops.base.group import Group
from mops.mixins.objects.locator import Locator


class SomeGroup(Group):
    def __init__(self, driver_wrapper = None):
        super().__init__(Locator('xpath=Group'), name='Group test_element_repr.py', driver_wrapper=driver_wrapper)

    some_element = Element('some_element')

def test_element_repr_playwright_one_driver(mocked_play_driver):
    pattern = (r'Element\(locator="id=some_element", name="some_element", parent=SomeGroup\) '
               r'at .*, 1_driver=<MagicMock id=.*>')
    assert re.search(pattern, repr(SomeGroup().some_element)), repr(SomeGroup().some_element)

def test_element_repr_selenium_one_driver(mocked_selenium_driver):
    pattern = (r'Element\(locator="id=some_element", name="some_element", parent=SomeGroup\) '
               r'at .*, 1_driver=<selenium.webdriver.remote.webdriver.WebDriver \(session="None"\)>')
    assert re.search(pattern, repr(SomeGroup().some_element)), repr(SomeGroup().some_element)

def test_element_repr_ios_one_driver(mocked_ios_driver):
    pattern = (r'Element\(locator="id=some_element", name="some_element", parent=SomeGroup\) '
               r'at .*, 1_driver=<appium.webdriver.webdriver.WebDriver \(session="None"\)>')
    assert re.search(pattern, repr(SomeGroup().some_element)), repr(SomeGroup().some_element)

def test_element_repr_android_one_driver(mocked_android_driver):
    pattern = (r'Element\(locator="id=some_element", name="some_element", parent=SomeGroup\) '
               r'at .*, 1_driver=<appium.webdriver.webdriver.WebDriver \(session="None"\)>')
    assert re.search(pattern, repr(SomeGroup().some_element)), repr(SomeGroup().some_element)

def test_element_repr_multiple_driver(
        mocked_play_driver,
        mocked_selenium_driver,
        mocked_ios_driver,
        mocked_android_driver
):
    obj_1_driver = repr(SomeGroup(driver_wrapper=mocked_play_driver).some_element)
    assert obj_1_driver.startswith('Element(locator="id=some_element", name="some_element", parent=SomeGroup) at')
    assert '1_driver=<MagicMock' in obj_1_driver

    obj_1_driver = repr(SomeGroup(driver_wrapper=mocked_selenium_driver).some_element)
    assert obj_1_driver.startswith('Element(locator="id=some_element", name="some_element", parent=SomeGroup) at')
    assert obj_1_driver.endswith('2_driver=<selenium.webdriver.remote.webdriver.WebDriver (session="None")>')

    obj_1_driver = repr(SomeGroup(driver_wrapper=mocked_ios_driver).some_element)
    assert obj_1_driver.startswith('Element(locator="id=some_element", name="some_element", parent=SomeGroup) at')
    assert obj_1_driver.endswith('3_driver=<appium.webdriver.webdriver.WebDriver (session="None")>')

    obj_1_driver = repr(SomeGroup(driver_wrapper=mocked_android_driver).some_element)
    assert obj_1_driver.startswith('Element(locator="id=some_element", name="some_element", parent=SomeGroup) at')
    assert obj_1_driver.endswith('4_driver=<appium.webdriver.webdriver.WebDriver (session="None")>')
