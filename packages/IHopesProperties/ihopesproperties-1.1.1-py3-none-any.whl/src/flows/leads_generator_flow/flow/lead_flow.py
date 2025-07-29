from typing import List

from apify.zillow_scrapers.zillow_detail_scraper.on_the_fly_runner import generate_for_sale_property_from_address
from common.utils.logger import log
from comps_extractor.comps_generator import generate_comps
from my_asana.tasks_generator import generate_new_property_task
from my_asana.utils import is_task_exists
from property import ForSaleProperty, SoldProperty

def address_based_lead_flow(address: str) -> str:
    lead_property: ForSaleProperty = generate_for_sale_property_from_address(address=address)
    property_link: str = lead_flow(lead_property)
    return property_link


def lead_flow(lead_property: ForSaleProperty) -> str:
    address: str = lead_property.address.get_full_address()
    log(msg=f'Working on property: {address}')

    if is_task_exists(address):
        log(msg=f"Task already exists for: {address}, stopping the process..")
        return ''

    lead_property: ForSaleProperty = generate_for_sale_property_from_address(address=address)
    log(msg=f"Generated a new for sale property successfully: {lead_property}")

    comps: List[SoldProperty] = generate_comps(
        for_sale_property=lead_property,
        test_mode=False
    )
    address: str = lead_property.address.get_full_address()
    log(f'Found total of {len(comps)} comps for {address}')

    if not comps:  # If no comps found, add to the no-comps list
        log(msg=f"No comps found for property: {address}.")

    property_link: str = generate_new_property_task(
        for_sale_property=lead_property,
        comps=comps
    )
    log(msg=f'Generated Asana task for {address} with link: {property_link}')

    return property_link
