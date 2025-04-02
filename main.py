from controller.controller import Controller
from constants.settings import Settings
from driver import initialize_driver

def main():
    headless: bool = Settings().HEADLESS
    browser_data = Settings().BROWSER_DATA
    browser = initialize_driver(headless=headless, user_data_dir=browser_data)
    page = browser.pages[0]
    controller = Controller(page)
    controller.run(Settings().USERNAME, Settings().PASSWORD, Settings().LIMIT)

if __name__ == "__main__":
    main()