import copy

from common.utils.logger import log
from property import PropertyAddress


def update_address_with_pittsburgh_ciy(address: PropertyAddress) -> PropertyAddress:
    """
    We might have cases where the property's address is written with a city such as Baden or Penn Hills in some places
     while in others it is listed with Pittsburgh as city.
    This usually can happen as the task is originally created using Rentcast API which will fetch the address as
     city=Baldwin, although in Zillow it will appear with City=Pittsburgh.
     Also, it might appear with city=Baldwin even in Redfin.
    :param address: Original address
    :return: Updated address with city set to Pittsburgh
    """
    log(msg=f"Got address: {address.get_full_address()}", app_log=False)
    address_copy: PropertyAddress = copy.deepcopy(address)
    address_copy.city = 'Pittsburgh'
    log(msg=f"Updated address: {address_copy.get_full_address()}", app_log=False)
    return address_copy
