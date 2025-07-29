from typing import Optional

from zillow.property_getter import construct_zillow_basic_property_url


class PropertyAddress:
    def __init__(self, address: str, city: str, state: str, zip_code: str):
        self.address: str = address
        self.city: str = city
        self.state: str = state
        self.zip_code: str = zip_code

    def get_full_address(self):
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"

    @staticmethod
    def from_full_address(full_address: str):
        """
        Address can either be '439 William St, Mount, Oliver, PA 15210' or '439 William St, PA 15210'.
        :param full_address:
        :return:
        """
        address_parts = full_address.split(',')
        if len(address_parts) == 4:
            address = address_parts[0].strip()
            city = f'{address_parts[1].strip()}, {address_parts[2].strip()}'
            state_zip = address_parts[3].strip().split()
            state = state_zip[0]
            zip_code = state_zip[1]
        elif len(address_parts) == 3:
            address = address_parts[0].strip()
            city = address_parts[1].strip()
            state_zip = address_parts[2].strip().split()
            state = state_zip[0]
            zip_code = state_zip[1]
        else:
            raise ValueError(f"Invalid address format: {full_address}")
        return PropertyAddress(address, city, state, zip_code)


class ListingAgent:
    def __init__(self, name: str, phone: str, email: str, website: Optional[str] = None):
        self.name: str = name
        self.phone: str = phone
        self.email: str = email
        self.website: Optional[str] = website



class Property:
    def __init__(self, address: PropertyAddress, beds: float, baths: float, sqft: int, lot_sqft: float,
                 lat: float, long: float, year_built: Optional[int] = None, zillow_link: Optional[str] = None):
        self.address: PropertyAddress = address
        self.bedrooms: float = beds
        self.bathrooms: float = baths
        self.sqft: int = sqft
        self.lot_sqft: float = lot_sqft
        self.lat: float = lat
        self.long: float = long
        self.year_built: Optional[int] = year_built
        self.zillow_link: str = zillow_link if zillow_link \
            else construct_zillow_basic_property_url(self.address.get_full_address())

    def get_min_sqft(self):
        """
        Consider up to 20% less than sqft
        :return:
        """
        return self.sqft * 0.8

    def get_max_sqft(self):
        """
        Consider up to 20% more than sqft
        :return:
        """
        return self.sqft * 1.2

    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great-circle distance between two points on the Earth's surface.

        Parameters:
        - lat1, lon1: Latitude and Longitude of point 1 in decimal degrees.
        - lat2, lon2: Latitude and Longitude of point 2 in decimal degrees.

        Returns:
        - Distance in miles.
        """
        # Earth radius in miles
        R = 3958.8

        # Convert latitude and longitude from degrees to radians
        import math
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Differences in latitude and longitude
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Haversine formula
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Distance in miles
        distance = R * c
        return distance


class ForSaleProperty(Property):
    def __init__(self, rentcast_pid: str, address: PropertyAddress, beds: float, baths: float,
                 sqft: int, lot_sqft: float, lat: float, long: float, year_built: int, asking_price: int,
                 listing_type: str, listed_date: str, days_on_market: int):
        super().__init__(
            address=address,
            beds=beds,
            baths=baths,
            sqft=sqft,
            lot_sqft=lot_sqft,
            year_built=year_built,
            lat=lat,
            long=long,
        )
        self.rentcast_pid: str = rentcast_pid
        self.asking_price: int = asking_price
        self.listing_type: str = listing_type
        self.listed_date: str = listed_date
        self.days_on_market: int = days_on_market

    def __eq__(self, other):
        return self.rentcast_pid == other.rentcast_pid

    def __hash__(self):
        return hash(self.rentcast_pid)


class SoldProperty(Property):
    def __init__(self, zillow_pid: str, address: PropertyAddress, beds: float, baths: float,
                 sqft: int, lot_sqft: float, lat: float, long: float, dist_from_lead: float, zillow_link: str,
                 sold_price: int, sold_date: str):
        super().__init__(
            address=address,
            beds=beds,
            baths=baths,
            sqft=sqft,
            lot_sqft=lot_sqft,
            lat=lat,
            long=long,
            zillow_link=zillow_link
        )
        self.dist_from_lead: float = dist_from_lead
        self.zillow_pid: str = zillow_pid
        self.sold_price: int = sold_price
        self.sold_date: str = sold_date
