import pytest
from configparser import ConfigParser
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from pages.login_page import LoginPage
from constants.login_constants import USERNAME_INPUT, PASSWORD_INPUT, LOGIN_BUTTON


def test_login_mocked(mocker):
    """
    Test the login functionality with mocked inputs and actions.
    """
    mocked_page = mocker.Mock()
    mocked_login_page = LoginPage(mocked_page)

    # Mock inputs
    username = "test_user"
    password = "test_password"
    
    # Call the login method
    mocked_login_page.login(username, password)
    
    # Assert that the correct methods were called with the correct arguments
    mocked_login_page.page.fill.assert_any_call(USERNAME_INPUT, username)
    mocked_login_page.page.fill.assert_any_call(PASSWORD_INPUT, password)
    mocked_login_page.page.click.assert_called_once_with(LOGIN_BUTTON)

def test_login_e2e(login_page: LoginPage, config: ConfigParser):
    """
    Test the end-to-end login functionality with real browser interaction.
    """
    # Retrieve valid credentials from config
    username = config.get("Settings", "username")
    password = config.get("Settings", "password")
    
    # Perform login
    assert login_page.get_username_locator().is_visible()
    login_page.login(username, password)
    assert login_page.get_username_locator().is_visible() == False

def test_invalid_login_e2e(login_page: LoginPage):
    """
    Test the login functionality with invalid credentials.
    """
    # Retrieve invalid credentials from config
    username = "invalid_username"
    password = "invalid_password"
    
    # Perform login
    assert login_page.get_username_locator().is_visible()
    login_page.login(username, password)
    login_page.page.wait_for_timeout(1000)
    assert login_page.get_username_locator().is_visible()