from controller.controller import Controller
from constants.settings import Settings
from driver import initialize_driver
import utils.logger


def main():
    headless: bool = Settings().HEADLESS
    browser_data = Settings().BROWSER_DATA
    browser_type = Settings().BROWSER_TYPE
    browser = initialize_driver(headless=headless, user_data_dir=browser_data, browser_type=browser_type)
    page = browser.pages[0]
    controller = Controller(page)
    controller.run(Settings().USERNAME, Settings().PASSWORD, Settings().LIMIT)

if __name__ == "__main__":
    main()