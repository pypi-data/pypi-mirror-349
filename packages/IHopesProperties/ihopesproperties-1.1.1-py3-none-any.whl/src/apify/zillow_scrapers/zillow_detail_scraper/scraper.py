import copy

from apify.zillow_scrapers.common.client import MyApifyClient
from apify.zillow_scrapers.common.config import Actor
from common.utils.address_maniplator import update_address_with_pittsburgh_ciy
from property import PropertyAddress


def scrape_zillow_with_retry(address: PropertyAddress) -> dict:
    property_data: dict = scrape_zillow(address.get_full_address())
    if not property_data['isValid']:
        # We might have different cities in the address, e.g. Baden vs. Pittsburgh. This can happen as the task is
        # originally created using Rentcast API which will fetch the address as city=Baldwin,
        # although in Zillow it will appear with City=Pittsburgh. Hence, we will first try to scrape the data with the
        # original city, and if it fails, we will try to scrape the data with the city set to Pittsburgh.
        print(f"Property data is not valid for: {address.get_full_address()}")
        updated_address: PropertyAddress = update_address_with_pittsburgh_ciy(address)
        property_data: dict = scrape_zillow(updated_address.get_full_address())
        if not property_data['isValid']:
            raise ValueError(f"Property data is not valid for: {updated_address.get_full_address()}")
    return property_data


def scrape_zillow(address: str) -> dict:
    """
    Scrape the Zillow website using the Zillow Detail Scraper actor.
    :param address:
    :return:
    """
    # Initialize the Apify client
    apify_client: MyApifyClient = MyApifyClient(actor=Actor.ZILLOW_DETAIL_SCRAPER)

    # Prepare the Actor input
    run_input = {
        "addresses": [address]
    }

    # Fetch and print Actor results from the run's dataset (if there are any)
    items: list = apify_client.run_client(run_input=run_input)
    if len(items) > 1:
        raise ValueError(f"Expected only one item in the list, but got {len(items)} items.")

    property_data: dict = items[0]
    return property_data
