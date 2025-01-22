import re

from selenium.webdriver.common.by import By

from mops.base.group import Group
from mops.mixins.objects.locator import Locator


class SomeGroup(Group):
    def __init__(self):
        super().__init__(Locator('Group', loc_type=By.XPATH), name='Group tests_element_repr.py')

def test_group_repr_playwright(mocked_play_driver):
    pattern = (r'SomeGroup\(locator="id=Group", name="Group tests_element_repr.py", parent=None\) '
               r'at .*, 1_driver=<MagicMock id=.*>')
    assert re.search(pattern, repr(SomeGroup()))

def test_group_repr_selenium(mocked_selenium_driver):
    pattern = (r'SomeGroup\(locator="Group", locator_type="xpath", name="Group tests_element_repr.py", parent=None\) '
               r'at .*, 1_driver=<selenium.webdriver.remote.webdriver.WebDriver \(session="None"\)>')
    assert re.search(pattern, repr(SomeGroup()))

def test_group_repr_ios(mocked_ios_driver):
    pattern = (r'SomeGroup\(locator="Group", locator_type="xpath", name="Group tests_element_repr.py", parent=None\) '
               r'at .*, 1_driver=<appium.webdriver.webdriver.WebDriver \(session="None"\)>')
    assert re.search(pattern, repr(SomeGroup()))

def test_group_repr_android(mocked_android_driver):
    pattern = (r'SomeGroup\(locator="Group", locator_type="xpath", name="Group tests_element_repr.py", parent=None\) '
               r'at .*, 1_driver=<appium.webdriver.webdriver.WebDriver \(session="None"\)>')
    assert re.search(pattern, repr(SomeGroup()))
