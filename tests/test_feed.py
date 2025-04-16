import pytest
from pages.feed_page import FeedPage
from constants.feed_constants import FEED_ITEMS 


def test_iterate_over_items_mocked(mocker):
    mock_page = mocker.Mock()
    mock_feed_page = FeedPage(mock_page)
    
    # Mock the locator and items
    mock_items = [mocker.Mock() for _ in range(5)]
    mock_search_results = mocker.Mock()
    mock_search_results.locator.return_value.all.return_value = mock_items
    mock_page.locator.return_value = mock_search_results
    
    # Mock the process_item function
    process_item = mocker.Mock(side_effect=lambda item: f"Processed {item}")
    
    # Call the method
    mock_feed_page.iterate_over_items(process_item, limit=3)
    
    # Assertions
    process_item.assert_called()
    assert process_item.call_count == 4  # 0, 1, 2, 3 (limit inclusive)
    mock_page.locator.assert_called_once_with(FEED_ITEMS)
    mock_search_results.locator.return_value.all.assert_called_once()

def test_iterate_over_items_e2e(feed_page: FeedPage):
    def process_item(item):
        item.click()
        return
    feed_page.iterate_over_items(process_item=process_item, limit=3)