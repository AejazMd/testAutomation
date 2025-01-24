import os
import pytest
from selenium import webdriver

# Replace hardcoded URLs and credentials with environment variables
LOGIN_URL = os.environ.get("LOGIN_URL", "http://default_login_url.com")
VALID_USERNAME = os.environ.get("VALID_USERNAME")
VALID_PASSWORD = os.environ.get("VALID_PASSWORD")

# Test data for various login scenarios
test_data = [
    (VALID_USERNAME, VALID_PASSWORD, True, "Dashboard"),  # Valid credentials
    ("invalid_user", "wrong_pass", False, "Invalid credentials"),  # Invalid credentials
    (VALID_USERNAME, "wrong_pass", False, "Invalid credentials"),  # Invalid password
    ("invalid_user", VALID_PASSWORD, False, "Invalid credentials"),  # Invalid username
]

@pytest.fixture(scope='module')
def setup_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.mark.parametrize("username, password, expected_success, expected_message", test_data)
def test_login(setup_driver, username, password, expected_success, expected_message):
    driver = setup_driver
    driver.get(LOGIN_URL)

    # Find elements and interact with them (replace with appropriate selectors)
    username_field = driver.find_element_by_name("username") # Replace with actual locator
    password_field = driver.find_element_by_name("password") # Replace with actual locator
    login_button = driver.find_element_by_name("login") # Replace with actual locator

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    if expected_success:
        assert expected_message in driver.title, f"Expected '{expected_message}' in title, but got '{driver.title}'"
        # Add tests for dashboard functionalities here
        # Example: Check for a specific element on the dashboard
        dashboard_element = driver.find_element_by_id("dashboard-element")  # Replace with actual locator
        assert dashboard_element.is_displayed(), "Dashboard element not found"
    else:
        assert expected_message in driver.page_source, f"Expected '{expected_message}' in page source, but got '{driver.page_source}'"