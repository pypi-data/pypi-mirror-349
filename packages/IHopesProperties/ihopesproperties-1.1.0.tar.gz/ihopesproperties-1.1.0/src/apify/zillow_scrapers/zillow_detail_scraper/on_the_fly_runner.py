from apify.zillow_scrapers.zillow_detail_scraper.scraper import scrape_zillow_with_retry
from property import ForSaleProperty, PropertyAddress


def generate_for_sale_property_from_address(address: str) -> ForSaleProperty:
    """
    Generate a ForSaleProperty object from the address.
    :param address:
    :return:
    """

    property_data: dict = scrape_zillow_with_retry(PropertyAddress.from_full_address(address))
    address_dict: dict = property_data['address']
    property_address: PropertyAddress = PropertyAddress(
        address=address_dict['streetAddress'],
        city=address_dict['city'],
        state=address_dict['state'],
        zip_code=address_dict['zipcode']
    )

    return ForSaleProperty(
        address=property_address,
        beds=property_data['bedrooms'],
        baths=property_data['bathrooms'],
        lat=property_data['latitude'],
        long=property_data['longitude'],
        sqft=property_data['livingArea'],
        lot_sqft=property_data['lotSize'],
        year_built=property_data['yearBuilt'],
        asking_price=property_data['price'],
        rentcast_pid="NA",
        listing_type="NA",
        listed_date="NA",
        days_on_market=0
    )
