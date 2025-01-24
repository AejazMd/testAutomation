import pytest
from selenium import webdriver
import os

# Retrieve credentials from environment variables
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
BASE_URL = os.environ.get("BASE_URL")

# Test data for parameterized testing
test_data = [
    (USERNAME, PASSWORD, "Dashboard"),  # Valid credentials
    ("invaliduser", "invalidpass", "Invalid credentials"),  # Invalid credentials
]

@pytest.fixture(scope="module")
def setup_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.mark.parametrize("username, password, expected_message", test_data)
def test_login(setup_driver, username, password, expected_message):
    driver = setup_driver
    driver.get(BASE_URL + "/login")  # Append login path to base URL
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()
    assert expected_message in driver.page_source, f"Expected '{expected_message}' in page source for credentials: {username}, {password}"

@pytest.mark.parametrize("username, password, expected_message", [(USERNAME, PASSWORD, "Dashboard")]) # Valid credentials to access Dashboard functionalities
def test_dashboard_functionalities(setup_driver, username, password, expected_message):
    driver = setup_driver
    driver.get(BASE_URL + "/login")
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()

    # Check for key dashboard elements
    assert "Welcome" in driver.page_source, "'Welcome' message not found on dashboard"
    assert "Settings" in driver.page_source, "'Settings' link not found on dashboard"

    # Test a specific dashboard action (example)
    driver.find_element_by_link_text("Settings").click()
    assert "User settings" in driver.title, "Navigation to User settings failed"