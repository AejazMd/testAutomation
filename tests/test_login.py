import pytest
from selenium import webdriver
import os

# Use environment variables for credentials and URL
LOGIN_URL = os.environ.get("LOGIN_URL", "http://default_login_url")
VALID_USERNAME = os.environ.get("VALID_USERNAME")
VALID_PASSWORD = os.environ.get("VALID_PASSWORD")

# Test data for various login scenarios
login_data = [
    (VALID_USERNAME, VALID_PASSWORD, "Dashboard", True),
    ("invaliduser", "invalidpass", "Invalid credentials", False),
    (VALID_USERNAME, "invalidpass", "Invalid credentials", False),
    ("", VALID_PASSWORD, "Username is required", False),
]

@pytest.fixture(scope='module')
def setup_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.mark.parametrize("username, password, expected_message, login_success", login_data)
def test_login_scenarios(setup_driver, username, password, expected_message, login_success):
    driver = setup_driver
    driver.get(LOGIN_URL)

    # Find elements and interact
    username_field = driver.find_element_by_name("username")  # Replace with actual locator
    password_field = driver.find_element_by_name("password")
    login_button = driver.find_element_by_name("login")

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    if login_success:
        assert expected_message in driver.title, f"Expected '{expected_message}' in title, but got '{driver.title}'"
        # Add tests for dashboard functionalities here
        # Example: Check if a specific element exists on the dashboard
        dashboard_element = driver.find_element_by_id("dashboard-element") # Replace with actual locator
        assert dashboard_element.is_displayed(), "Dashboard element not found"

        # Example: Check if a specific action can be performed on the dashboard
        # ...
    else:
        assert expected_message in driver.page_source, f"Expected '{expected_message}' in page source, but got '{driver.page_source}'"