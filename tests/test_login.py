import pytest
from selenium import webdriver
import os

# Retrieve environment variables
base_url = os.environ.get("BASE_URL", "http://example.com")  # Default if not set
valid_username = os.environ.get("VALID_USERNAME")
valid_password = os.environ.get("VALID_PASSWORD")
invalid_username = os.environ.get("INVALID_USERNAME", "wronguser")
invalid_password = os.environ.get("INVALID_PASSWORD", "wrongpass")

@pytest.fixture(scope='module')
def setup_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Positive test cases for login
@pytest.mark.parametrize("username, password, expected_title", [
    (valid_username, valid_password, "Dashboard"),
    ("testuser2", "password123", "Dashboard")  # Additional test case
])
def test_valid_login(setup_driver, username, password, expected_title):
    driver = setup_driver
    driver.get(f"{base_url}/login")
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()
    assert expected_title in driver.title, f"Expected title '{expected_title}' but got '{driver.title}'"

# Negative test cases for login
@pytest.mark.parametrize("username, password, expected_message", [
    (invalid_username, invalid_password, "Invalid credentials"),
    (valid_username, invalid_password, "Invalid credentials"),
    (invalid_username, valid_password, "Invalid credentials")
])
def test_invalid_login(setup_driver, username, password, expected_message):
    driver = setup_driver
    driver.get(f"{base_url}/login")
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()
    assert expected_message in driver.page_source, f"Expected message '{expected_message}' not found on page."


# Test dashboard functionalities (assuming successful login)
def test_dashboard_elements(setup_driver):
    driver = setup_driver
    driver.get(f"{base_url}/dashboard")  # Assuming direct dashboard URL for demo
    assert "Welcome" in driver.page_source  # Check for welcome message
    assert "Logout" in driver.page_source  # Check for logout button