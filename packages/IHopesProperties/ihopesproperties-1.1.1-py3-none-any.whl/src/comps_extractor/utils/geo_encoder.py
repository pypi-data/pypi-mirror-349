from typing import Optional

import requests
import random
from comps_extractor.utils.coordinates import AddressCoordinates
from property import PropertyAddress


def get_coordinates(address: PropertyAddress) -> Optional[AddressCoordinates]:
    """
    Use the Nominatim API to get the latitude and longitude of an address.
    Consider add sleep time to avoid rate limiting.
    :param address: without zip code, e.g. "152 W Patty Ln, Monroeville, PA"
    :return: latitude and longitude
    """
    base_url = "https://nominatim.openstreetmap.org/search"

    headers = {
        "User-Agent": random.choice(["25to40", "IHopes", "IHopesProperties", "25to40IHopesProperties"])
    }

    params = {
        "q": address,
        "format": "json"
    }

    params = {
        "street": address.address,
        "city": address.city,
        "state": address.state,
        "country": "USA",
        "format": "json",
    }

    response = requests.get(base_url, params=params, headers=headers)
    data = response.json()

    if data:
        location = data[0]
        latitude: float = float(location["lat"])
        longtitude: float = float(location["lon"])
        print(f"Coordinates for {address}: Latitude={latitude}, Longitude={longtitude}")

        return AddressCoordinates(
            address=address.get_full_address(),
            lat=latitude,
            lon=longtitude
        )
    else:
        print(f"No coordinates found for {address}")
        return None
