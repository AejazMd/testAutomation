import pytest
import os
from selenium import webdriver

# Load credentials from environment variables
valid_username = os.getenv('TEST_VALID_USERNAME', 'testuser')
valid_password = os.getenv('TEST_VALID_PASSWORD', 'password123')
invalid_username = os.getenv('TEST_INVALID_USERNAME', 'wronguser')
invalid_password = os.getenv('TEST_INVALID_PASSWORD', 'wrongpass')

@pytest.fixture(scope='module')
def setup_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Positive test case for login
@pytest.mark.parametrize('username, password', [(valid_username, valid_password)])
def test_login_positive(setup_driver, username, password):
    driver = setup_driver
    driver.get(os.getenv('LOGIN_URL', 'http://example.com/login'))
    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('login').click()
    assert 'Dashboard' in driver.title, 'Dashboard not found after successful login'

# Negative test case for login
@pytest.mark.parametrize('username, password', [(invalid_username, invalid_password)])
def test_login_negative(setup_driver, username, password):
    driver = setup_driver
    driver.get(os.getenv('LOGIN_URL', 'http://example.com/login'))
    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('login').click()
    assert 'Invalid credentials' in driver.page_source, 'Error message not displayed for invalid login'

# Additional tests for dashboard functionalities

# Test check for key elements in dashboard
@pytest.mark.parametrize('element', ['profile', 'settings', 'logout'])
def test_dashboard_elements(setup_driver, element):
    driver = setup_driver
    driver.get('http://example.com/dashboard')
    assert driver.find_element_by_id(element), f'{element.capitalize()} element not found on dashboard.'