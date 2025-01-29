from types import SimpleNamespace

import pytest
from selenium.webdriver.common.by import By

from mops.utils.selector_synchronizer import set_selenium_selector, set_playwright_locator


@pytest.mark.parametrize(
    "locator_input, expected_locator, expected_locator_type, expected_log_locator",
    [
        ("xpath=//div", "//div", By.XPATH, "xpath=//div"),
        ("text=Hello", '//*[contains(text(), "Hello")]', By.XPATH, "text=Hello"),
        ("css=.class", ".class", By.CSS_SELECTOR, "css=.class"),
        ("id=my_id", '[id="my_id"]', By.CSS_SELECTOR, "id=my_id"),
        ("/html/body/div", "/html/body/div", By.XPATH, "xpath=/html/body/div"),
        ("#my_element", "#my_element", By.CSS_SELECTOR, "css=#my_element"),
        ("button", "button", By.CSS_SELECTOR, "css=button"),
        ("tbody tr td span", "tbody tr td span", By.CSS_SELECTOR, "css=tbody tr td span"),
        ("textarea", "textarea", By.CSS_SELECTOR, "css=textarea"),
        ("Some text", '//*[contains(text(), "Some text")]', By.XPATH, 'xpath=//*[contains(text(), "Some text")]'),
        ("[href='/some/url']", "[href='/some/url']", By.CSS_SELECTOR, "css=[href='/some/url']"),
    ],
)
def test_set_selenium_selector(locator_input, expected_locator, expected_locator_type, expected_log_locator):
    mock_obj = SimpleNamespace()
    mock_obj.locator = locator_input
    set_selenium_selector(mock_obj)
    assert expected_locator == mock_obj.locator
    assert expected_log_locator == mock_obj.log_locator


@pytest.mark.parametrize(
    "locator_input, expected_locator",
    [
        ("xpath=//div", "xpath=//div"),
        ("text=Hello", "text=Hello"),
        ("css=.class", "css=.class"),
        ("id=my_id", "id=my_id"),
        ("/html/body/div", "xpath=/html/body/div"),
        ("#my_element", "css=#my_element"),
        ("button", "css=button"),
        ("tbody tr td span", "css=tbody tr td span"),
        ("Some text", "text=Some text"),
        ("[href='/some/url']", "css=[href='/some/url']"),
    ],
)
def test_set_playwright_locator(locator_input, expected_locator):
    mock_obj = SimpleNamespace()
    mock_obj.locator = locator_input
    set_playwright_locator(mock_obj)
    assert expected_locator == mock_obj.locator
    assert expected_locator == mock_obj.log_locator
    assert expected_locator.partition('=')[0] == mock_obj.locator_type
