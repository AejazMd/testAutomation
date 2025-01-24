import pytest
import os
from selenium import webdriver

# Environment variables for login credentials
valid_username = os.getenv('VALID_USERNAME')
valid_password = os.getenv('VALID_PASSWORD')
invalid_username = 'wronguser'
invalid_password = 'wrongpass'

@pytest.fixture(scope='module')
def setup_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Parameterized tests for login scenarios
@pytest.mark.parametrize('username,password,should_pass', [
    (valid_username, valid_password, True),
    (invalid_username, invalid_password, False),
])
def test_login(setup_driver, username, password, should_pass):
    driver = setup_driver
    driver.get(os.getenv('LOGIN_URL'))
    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('login').click()
    if should_pass:
        assert 'Dashboard' in driver.title, "Login should succeed but didn't."
    else:
        assert 'Invalid credentials' in driver.page_source, "Login should fail but succeeded."

# Add tests for specific dashboard functionalities
def test_dashboard_elements(setup_driver):
    driver = setup_driver
    driver.get(os.getenv('DASHBOARD_URL'))
    assert driver.find_element_by_id('welcome-message').is_displayed(), "Welcome message should be displayed."
    assert driver.find_element_by_id('logout-button').is_displayed(), "Logout button should be displayed."