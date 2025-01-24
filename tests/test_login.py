import pytest
from selenium import webdriver
import os

# Retrieve environment variables
LOGIN_URL = os.environ.get("LOGIN_URL")
VALID_USERNAME = os.environ.get("VALID_USERNAME")
VALID_PASSWORD = os.environ.get("VALID_PASSWORD")

# Test data using parameterized testing
@pytest.mark.parametrize("username, password, expected_title", [
    (VALID_USERNAME, VALID_PASSWORD, "Dashboard"),
    ("invaliduser", "wrongpass", "Login"), # Invalid credentials
    (VALID_USERNAME, "wrongpass", "Login"),  # Incorrect password
    ("invaliduser", VALID_PASSWORD, "Login") # Incorrect username
])
def test_login_scenarios(setup_driver, username, password, expected_title):
    driver = setup_driver
    driver.get(LOGIN_URL)
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()
    assert expected_title in driver.title, f"Expected title: {expected_title}, Actual title: {driver.title}"

@pytest.fixture(scope="module")
def setup_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Test specific dashboard functionalities (assuming successful login)
def test_dashboard_elements(setup_driver):
    driver = setup_driver
    driver.get(LOGIN_URL)
    driver.find_element_by_name("username").send_keys(VALID_USERNAME)
    driver.find_element_by_name("password").send_keys(VALID_PASSWORD)
    driver.find_element_by_name("login").click()

    # Check for key dashboard elements
    assert "Welcome" in driver.page_source, "Welcome message not found on dashboard"
    assert "Logout" in driver.page_source, "Logout button not found on dashboard"
    try:
        driver.find_element_by_id("dashboard-calendar") # Replace with a relevant element ID from your dashboard
    except Exception as e:
        pytest.fail(f"Dashboard calendar element not found: {str(e)}")