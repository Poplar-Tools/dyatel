import pytest
from selenium.webdriver.common.by import By

from mops.base.element import Element
from mops.mixins.objects.locator import Locator
from mops.utils.internal_utils import all_tags
from tests.static_tests.conftest import selenium_ids, selenium_drivers, all_drivers, all_ids

tags = {'header h4', *all_tags}


@pytest.mark.parametrize('locator', ('.element', '[id *= element]', 'div#some_id'))
@pytest.mark.parametrize('driver', selenium_drivers, ids=selenium_ids)
def test_base_class_auto_css_locator(locator, request, driver):
    request.getfixturevalue(driver)
    assert Element(locator).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('locator', tags)
def test_base_class_auto_tag_name_locator(locator, mocked_selenium_driver):
    assert Element(locator).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('locator', tags)
def test_base_class_auto_tag_name_locator_mobile(locator, mocked_android_driver):
    assert Element(locator).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('locator', ('//a', '/b', '//*[@contains(@class, "name") and .="name"]'))
@pytest.mark.parametrize('driver', selenium_drivers, ids=selenium_ids)
def test_base_class_auto_xpath_locator(locator, driver, request):
    request.getfixturevalue(driver)
    assert Element(locator).locator_type == By.XPATH


@pytest.mark.parametrize('locator', ('some-id', 'example__of--id'))
def test_base_class_auto_id_locator_web(locator, mocked_selenium_driver):
    assert Element(locator).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('locator', ('some-id', 'example__of--id', 'com.android.chrome:id/bottom_container'))
def test_base_class_auto_id_locator_mobile(locator, mocked_android_driver):
    assert Element(locator).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('driver', selenium_drivers, ids=selenium_ids)
def test_specify_css_locator_type(request, driver):
    request.getfixturevalue(driver)
    assert Element(Locator('[href="/loaddelay"]')).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('locator', tags)
def test_specify_class_name_locator_type_mobile(locator, mocked_selenium_driver):
    assert Element(Locator(locator)).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('locator', tags)
def test_specify_class_name_locator_type_web(locator, mocked_android_driver):
    assert Element(locator).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('driver', selenium_drivers, ids=selenium_ids)
def test_name_missed(request, driver):
    request.getfixturevalue(driver)
    locator = '.sample .locator'
    assert Element(locator).name == locator


@pytest.mark.parametrize('driver', all_drivers, ids=all_ids)
def test_name_specified(request, driver):
    request.getfixturevalue(driver)
    locator, name = '.sample .locator', 'sample name'
    assert Element(locator, name=name).name == name
