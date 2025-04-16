import logging
from configparser import ConfigParser
import pytest
from playwright.sync_api import sync_playwright, BrowserContext, Page
from typing import Generator
from pages import LoginPage
from pages import ItemPage
from pages import FeedPage
from unittest.mock import MagicMock
from utils.msg_gen import MessageGenerator
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)
load_dotenv()


@pytest.fixture(scope="session")
def config() -> ConfigParser:
    config = ConfigParser()
    config.read('pytest.ini')
    return config

@pytest.fixture(scope="session")
def playwright_instance() -> Generator:
    logger.info("Starting Playwright instance...")
    instance = sync_playwright().start()
    yield instance
    logger.info("Stopping Playwright instance...")
    instance.stop()
    logger.info("Playwright instance stopped.")

@pytest.fixture(scope="session")
def playwright_browser(config: ConfigParser, playwright_instance) -> Generator[BrowserContext, None, None]:
    try:
        logger.info("Launching persistent Playwright browser context...")
        HEADLESS = config.getboolean("Settings", "headless")
        browser_context = playwright_instance.webkit.launch_persistent_context(
            user_data_dir=config.get("Settings", "browser_data_dir"),
            headless=HEADLESS
        )
        logger.info("Persistent browser context launched successfully.")
        yield browser_context
        logger.info("Closing persistent browser context...")
        browser_context.close()
        logger.info("Persistent browser context closed.")
    except Exception as e:
        logger.error(f"Failed to launch persistent browser context: {e}")
        raise

@pytest.fixture(scope="session")
def playwright_browser_no_data(playwright_instance, config: ConfigParser) -> Generator[BrowserContext, None, None]:
    try:
        logger.info("Launching persistent Playwright browser context...")
        HEADLESS = config.getboolean("Settings", "headless")
        browser_context = playwright_instance.webkit.launch(headless=HEADLESS)
        logger.info("Persistent browser context launched successfully.")
        yield browser_context
        logger.info("Closing persistent browser context...")
        browser_context.close()
        logger.info("Persistent browser context closed.")
    except Exception as e:
        logger.error(f"Failed to launch persistent browser context: {e}")
        raise

@pytest.fixture(scope="function")
def playwright_page(playwright_browser: BrowserContext) -> Generator[Page, None, None]:
    page = playwright_browser.pages[0] if playwright_browser.pages else playwright_browser.new_page()
    logger.info("Navigating to test page...")
    page.goto("about:blank")
    logger.info("Test page loaded successfully.")
    yield page
    page.close()

@pytest.fixture(scope="function")
def playwright_page_no_data(playwright_browser_no_data: BrowserContext) -> Generator[Page, None, None]:
    page = playwright_browser_no_data.new_page()
    logger.info("Navigating to test page...")
    page.goto("about:blank")
    logger.info("Test page loaded successfully.")
    yield page
    page.close()
    
@pytest.fixture(scope="function")
def login_page(playwright_page_no_data):
    return LoginPage(playwright_page_no_data)

@pytest.fixture(scope="function")
def feed_page(playwright_page):
    return FeedPage(playwright_page)

@pytest.fixture(scope="function")
def item_page(playwright_page, config):
    TEST_ID = config.get("Settings", "test_id")
    return ItemPage(playwright_page, TEST_ID)

@pytest.fixture
def mock_llm_utils(mocker):
    mock_llm = mocker.patch('utils.msg_gen.LLMUtils')
    mock_llm_instance = mock_llm.return_value
    mock_llm_instance.generate_text.return_value = "Generated text"
    return mock_llm_instance

@pytest.fixture
def message_generator():
    api_key = os.getenv("API_KEY")
    return MessageGenerator(api_key=api_key)