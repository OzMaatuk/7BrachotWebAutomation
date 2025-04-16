from playwright.sync_api import sync_playwright, BrowserContext

def initialize_driver(headless: bool = True, user_data_dir: str = None) -> BrowserContext:
    playwright = sync_playwright().start()
    browser = playwright.webkit.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=headless,
                ignore_https_errors=True)
    return browser
