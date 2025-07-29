from apify.zillow_scrapers.zillow_detail_scraper.scraper import scrape_zillow_with_retry
from flows.under_contract_follow_up_flow.contingent_status_handlers import ContingentStatus
from flows.under_contract_follow_up_flow.under_contract_task import UnderContractTask
from property import PropertyAddress


def get_contingency_status(under_contract_task: UnderContractTask) -> ContingentStatus:
    """
    Run the Apify Zillow scraper using the Apify client.
    :param under_contract_task: The under contract property to scrape.
    :return: Details of the scraper execution, including a link to the dataset.
    """

    return get_contingency_status_by_address(under_contract_task.address)


def get_contingency_status_by_address(property_address: PropertyAddress) -> ContingentStatus:
    """
    Run the Apify Zillow scraper using the Apify client.
    :param property_address: The address of the property to scrape.
    :return: Details of the scraper execution, including a link to the dataset.
    """

    property_data: dict = scrape_zillow_with_retry(property_address)
    contingency_status: ContingentStatus = transform_property_data_to_contingency_status(property_data)
    return contingency_status


def transform_property_data_to_contingency_status(property_data: dict) -> ContingentStatus:
    """
    Transform the response data from the Zillow scraper into a ContingentStatus object.
    :param property_data:
    :return:
    """
    still_under_contract: bool = (property_data['contingentListingType'] == 'UNDER_CONTRACT' or
                                  property_data['homeStatus'] == 'PENDING')

    is_for_sale: bool = property_data['homeStatus'] == 'FOR_SALE'

    is_sold: bool = property_data['homeStatus'] == 'RECENTLY_SOLD' or property_data['homeStatus'] == 'SOLD' or \
                    property_data['homeStatus'] == 'FORECLOSED'

    is_off_market: bool = property_data['homeStatus'] == 'OTHER' and property_data['adTargets']['listtp'] == 'not_for_sale'

    if not any([still_under_contract, is_for_sale, is_sold, is_off_market]):
        print(f"Property data: {property_data}")
        raise ValueError(f"Could not determine the status of the property: {property_data}")

    if still_under_contract:
        return ContingentStatus.UNDER_CONTRACT
    elif is_for_sale:
        return ContingentStatus.FOR_SALE
    elif is_sold:
        return ContingentStatus.RECENTLY_SOLD
    elif is_off_market:
        return ContingentStatus.OFF_MARKET
    else:
        raise ValueError(f"Could not determine the status of the property: {property_data}")
