import pytest
from selenium import webdriver
import os

# Replace hardcoded URLs and credentials with environment variables
LOGIN_URL = os.environ.get("LOGIN_URL", "http://example.com/login") # Provide a default for local testing
VALID_USERNAME = os.environ.get("VALID_USERNAME")
VALID_PASSWORD = os.environ.get("VALID_PASSWORD")

# Test data for various login scenarios
test_data = [
    (VALID_USERNAME, VALID_PASSWORD, "Dashboard", True), # Valid credentials
    ("wronguser", "wrongpass", "Invalid credentials", False), # Invalid credentials
    (VALID_USERNAME, "wrongpass", "Invalid credentials", False), # Invalid password
    ("wronguser", VALID_PASSWORD, "Invalid credentials", False), # Invalid username
    ("", "", "Username is required", False), # Empty username and password
    (VALID_USERNAME, "", "Password is required", False)  # Empty password

]

@pytest.fixture(scope='module')
def setup_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.mark.parametrize("username, password, expected_message, positive_test", test_data)
def test_login(setup_driver, username, password, expected_message, positive_test):
    driver = setup_driver
    driver.get(LOGIN_URL)
    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('login').click()
    if positive_test:
        assert expected_message in driver.title, f"Expected '{expected_message}' in title, but got '{driver.title}'"
        # Add tests for specific dashboard functionalities:
        assert "Welcome" in driver.page_source
        assert "Logout" in driver.page_source
        try:  # Check for a clickable action or a specific element
           driver.find_element_by_link_text("Settings") 
        except Exception as e:
            print(f"Element not found or action failed: {e}")
            assert False

    else:
        assert expected_message in driver.page_source, f"Expected '{expected_message}' in page source, but got '{driver.page_source}'"