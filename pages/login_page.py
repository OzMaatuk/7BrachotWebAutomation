import logging
from playwright.sync_api import Page
from constants.login_constants import USERNAME_INPUT, PASSWORD_INPUT, LOGIN_BUTTON
from constants.settings import Settings
logger = logging.getLogger(__name__)

class LoginPage:
    def __init__(self, page: Page):
        logger.debug("Initiliazing LoginPage")
        self.page = page
        self.page.goto(Settings().BASE_URL)
        self.page.wait_for_load_state(state="networkidle")

    def is_logged_in(self) -> bool:
        logger.debug("LoginPage.is_logged_in")
        try:
            self.page.locator(USERNAME_INPUT).wait_for(1000)
            return False
        except Exception:
            # self.page.locator(FEED_ITEMS).wait_for(1000)
            return True

    def login(self, username: str, password: str):
        logger.debug("LoginPage.login")
        if self.is_logged_in(): return
        self.page.fill(USERNAME_INPUT, username)
        self.page.fill(PASSWORD_INPUT, password)
        self.page.click(LOGIN_BUTTON)

    def get_username_locator(self):
        logger.debug("LoginPage.get_username_locator")
        return self.page.locator(USERNAME_INPUT)
    
    def get_password_locator(self):
        logger.debug("LoginPage.get_username_locator")
        return self.page.locator(USERNAME_INPUT)
    
    def get_username_locator(self):
        logger.debug("LoginPage.get_username_locator")
        return self.page.locator(USERNAME_INPUT)