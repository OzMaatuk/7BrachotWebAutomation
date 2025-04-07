from types import FunctionType
from playwright.sync_api import Page
from constants.settings import Settings
from pages.login_page import LoginPage
from pages.feed_page import FeedPage
from pages.item_page import ItemPage
import logging
logger = logging.getLogger(__name__)

class Facade:
    def __init__(self, page):
        logger.debug("Initiliazing Facade")
        self.page = page

    def login(self, username: str, password: str):
        logger.debug("Facade.login")
        login_page = LoginPage(self.page)
        self.page.goto(Settings().BASE_URL)
        login_page.login(username, password)

    def get_num_of_views(self) -> int:
        return FeedPage(self.page).get_num_of_views()    

    def collect_items(self, filter: FunctionType, extract: FunctionType, limit: int = None, viewed_my_profile: bool = False):
        logger.debug("Facade.collect_items")
        feed_page = FeedPage(page=self.page, viewed_my_profile=viewed_my_profile)

        def process_item(page, item):
            try:
                if filter(page, item):
                    item.click()
                    return extract(page, item)
            except Exception as e:
                logger.error(f"Error processing item: {e}")
            return None
        
        res = feed_page.iterate_over_items(process_item, limit)
        return [item for item in (res or []) if item is not None]
    
    def apply_filters(self, filters: dict):
        logger.debug("Facade.apply_filters")
        feed_page = FeedPage(self.page)
        try:
            feed_page.filter_min_age(filters['min_age'])
        except Exception as e:
            logger.error(f"Error applying min_age filter: {e}")
        try:
            feed_page.filter_min_age(filters['max_age'])
        except Exception as e:
            logger.error(f"Error applying max_age filter: {e}")
        try:
            feed_page.filter_high(filters['high'])
        except Exception as e:
            logger.error(f"Error applying high filter: {e}")
        # TODO
        pass
    
    def item_action(page: Page, id: str, create_message: FunctionType):
        logger.debug("Facade.operate_on_item")
        try:
            item_page = ItemPage(page, id)
            item_details = item_page.get_info()
            msg = create_message(item_details)
            item_page.send_message(msg)
        except Exception as e:
            logger.error(f"Error performing action on item {id}: {e}")

    def filter_item(page, item, filter_description: str = None):
        if not filter_description:
            filter_description = "just answer yes."
        # TODO: should use llm to filter items
        return True

    def extract_id(page, item):
        id = page.url.split('/')[-1][6:][:-1]
        if len(id) in range(30, 50):
            return id
        logger.error("Could not extract item id.")
        return None

    def close(self):
        pass