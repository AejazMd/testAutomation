import pytest
from selenium import webdriver

# Dummy test data
valid_username = 'testuser'
valid_password = 'password123'
invalid_username = 'wronguser'
invalid_password = 'wrongpass'

@pytest.fixture(scope='module')
def setup_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Positive test case for login
@pytest.mark.parametrize('username, password', [(valid_username, valid_password)])
def test_login_positive(setup_driver, username, password):
    driver = setup_driver
    driver.get('http://example.com/login')
    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('login').click()
    assert 'Dashboard' in driver.title

# Negative test case for login
@pytest.mark.parametrize('username, password', [(invalid_username, invalid_password)])
def test_login_negative(setup_driver, username, password):
    driver = setup_driver
    driver.get('http://example.com/login')
    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('login').click()
    assert 'Invalid credentials' in driver.page_source