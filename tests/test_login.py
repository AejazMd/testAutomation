import pytest
from selenium import webdriver
import os

# Retrieve credentials from environment variables
valid_username = os.environ.get("VALID_USERNAME")
valid_password = os.environ.get("VALID_PASSWORD")
invalid_username = os.environ.get("INVALID_USERNAME")
invalid_password = os.environ.get("INVALID_PASSWORD")
login_url = os.environ.get("LOGIN_URL")

@pytest.fixture(scope="module")
def setup_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Test cases for login with different scenarios
@pytest.mark.parametrize("username, password, expected_title", [
    (valid_username, valid_password, "Dashboard"),
    (invalid_username, invalid_password, "Login"),
    (valid_username, invalid_password, "Login"),
    (invalid_username, valid_password, "Login"),
])
def test_login(setup_driver, username, password, expected_title):
    driver = setup_driver
    driver.get(login_url)
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()
    assert expected_title in driver.title, f"Expected title '{expected_title}' but got '{driver.title}'"

# Test cases for dashboard functionalities
def test_dashboard_elements(setup_driver):
    # Successful login is required before accessing the dashboard
    test_login(setup_driver, valid_username, valid_password, "Dashboard")

    driver = setup_driver
    # Check for key elements
    assert driver.find_element_by_id("welcome-message").is_displayed(), "Welcome message not displayed"
    assert driver.find_element_by_id("profile-link").is_displayed(), "Profile link not displayed"
    assert driver.find_element_by_id("settings-button").is_displayed(), "Settings button not displayed"

    # Example interaction: click on the settings button
    driver.find_element_by_id("settings-button").click()
    assert "Settings" in driver.title, "Navigation to settings page failed"