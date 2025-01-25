from mops.base.element import Element
from mops.base.group import Group
from mops.mixins.internal_mixin import get_element_info
from mops.mixins.objects.locator import Locator


class SomeGroup(Group):
    def __init__(self, driver_wrapper=None):
        super().__init__(Locator('group', ios='gielement', android='gaelement'), driver_wrapper=driver_wrapper)

    el = Element('element')
    mel = Element(
        Locator('delement', ios='ielement', android='aelement')
    )

    @property
    def another_group(self):
        return AnotherGroup(parent=self)


class AnotherGroup(Group):
    def __init__(self, parent):
        super().__init__('another_group', parent=parent)

    el = Element(Locator('another_element', ios='.another_i_element', android='.another_a_element'))


def test_get_element_info_selenium(mocked_selenium_driver):
    el = Element('element')
    assert "Selector: 'id=element'" in get_element_info(el)


def test_get_element_info_with_parent_selenium(mocked_selenium_driver):
    el = SomeGroup().another_group.el
    assert "Selector: 'id=another_element' <= 'id=another_group' <= 'id=group'" in get_element_info(el)

def test_get_element_info_playwright(mocked_play_driver):
    el = Element('element')
    assert "Selector: 'id=element'" in get_element_info(el)


def test_get_element_info_with_parent_playwright(mocked_play_driver):
    el = SomeGroup().another_group.el
    assert "Selector: 'id=another_element' <= 'id=another_group' <= 'id=group'" in get_element_info(el)


def test_get_element_info_with_ios(mocked_ios_driver):
    el = SomeGroup().mel
    assert "Selector: 'id=ielement' <= 'id=gielement'" in get_element_info(el)


def test_get_element_info_with_android(mocked_android_driver):
    el = SomeGroup().mel
    assert "Selector: 'id=aelement' <= 'id=gaelement" in get_element_info(el)


def test_get_element_info_with_parent_ios(mocked_ios_driver):
    el = SomeGroup().another_group.el
    assert "Selector: 'css=.another_i_element' <= 'id=another_group' <= 'id=gielement'" in get_element_info(el)


def test_get_element_info_with_parent_android(mocked_android_driver):
    el = SomeGroup().another_group.el
    assert "Selector: 'css=.another_a_element' <= 'id=another_group' <= 'id=gaelement'" in get_element_info(el)


def test_get_element_info_with_mobile_and_desktop(mocked_android_driver, mocked_selenium_driver):
    mobile_element = SomeGroup(driver_wrapper=mocked_android_driver).mel
    assert "Selector: 'id=aelement' <= 'id=gaelement'" in get_element_info(mobile_element)

    desktop_element = SomeGroup(driver_wrapper=mocked_selenium_driver).mel
    assert "Selector: 'id=delement' <= 'id=group'" in get_element_info(desktop_element)
