import pytest
from selenium import webdriver
import os

# Replace hardcoded URLs and credentials with environment variables
LOGIN_URL = os.environ.get("LOGIN_URL", "http://default_login_url")
VALID_USERNAME = os.environ.get("VALID_USERNAME")
VALID_PASSWORD = os.environ.get("VALID_PASSWORD")

# Test data for various login scenarios
@pytest.mark.parametrize("username, password, expected_result", [
    (VALID_USERNAME, VALID_PASSWORD, "Dashboard"),
    ("invalid", "password", "Invalid credentials"),
    (VALID_USERNAME, "invalid", "Invalid credentials"),
])
def test_login_scenarios(setup_driver, username, password, expected_result):
    driver = setup_driver
    driver.get(LOGIN_URL)
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()
    assert expected_result in driver.page_source, f"Expected '{expected_result}' in page source for credentials: {username}/{password}"

# Fixture for driver setup
@pytest.fixture(scope="module")
def setup_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Test for dashboard functionalities
def test_dashboard_elements(setup_driver):
    # Perform login with the valid credentials
    test_login_scenarios(setup_driver, VALID_USERNAME, VALID_PASSWORD, "Dashboard")

    driver = setup_driver
    # Check for key elements on the dashboard
    assert driver.find_element_by_id("welcome-message").is_displayed(), "Welcome message not displayed"
    assert driver.find_element_by_id("profile-link").is_displayed(), "Profile link not displayed"
    assert driver.find_element_by_id("settings-button").is_displayed(), "Settings button not displayed"