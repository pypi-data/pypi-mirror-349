from dataclasses import dataclass, Field
from typing import Optional, List

from pydantic import BaseModel, field_validator




class LeadQuerySource(BaseModel):
    zipcode: Optional[str] = None
    neighborhood: Optional[str] = None
    city: str
    state: str


    def to_string(self) -> str:
        if self.zipcode:
            return f'zipcode: {self.zipcode} of {self.neighborhood}'
        if self.city:
            return self.city


class LeadsQuerySourcesHolder:
    def __init__(self):
        self.leads_sources: List[LeadQuerySource] = [
            # Inner city neighborhoods by zip code
            # LeadQuerySource(zipcode=str(BEECHVIEW), neighborhood='Beechview', city='Pittsburgh', state='PA'),
            # LeadQuerySource(zipcode=str(BROOKLINE), neighborhood='Brookline', city='Pittsburgh', state='PA'),
            # LeadQuerySource(zipcode=str(MOUNT_WASHINGTON), neighborhood='Mount Washington', city='Pittsburgh', state='PA'),
            # LeadQuerySource(zipcode=str(BRIGHTON_HEIGHTS), neighborhood='Brighton Heights', city='Pittsburgh', state='PA'),
            # LeadQuerySource(zipcode=str(GREENFIELD), neighborhood='Greenfield', city='Pittsburgh', state='PA'),
            # LeadQuerySource(zipcode=str(BLOOMFIELD), neighborhood='Bloomfield', city='Pittsburgh', state='PA'),
            # LeadQuerySource(zipcode=str(SQUIRREL_HILL), neighborhood='Squirrel Hill', city='Pittsburgh', state='PA'),

            LeadQuerySource(city='Pittsburgh', state='PA'),

            # Outside city neighborhoods by city
            LeadQuerySource(city='Monroeville', state='PA'),
            LeadQuerySource(city='Whitehall', state='PA'),
            LeadQuerySource(city='Baldwin', state='PA'),
            LeadQuerySource(city='Carnegie', state='PA'),
            LeadQuerySource(city='Scott Township', state='PA'),
            LeadQuerySource(city='Bethel Park', state='PA'),
            LeadQuerySource(city='Avalon', state='PA'),
            LeadQuerySource(city='Bellevue', state='PA'),
        ]

    def get_source_by_city(self, city: str) -> Optional[LeadQuerySource]:
        """
        Get a lead source by city
        :param city:
        :return: A LeadQuerySource object if found, None otherwise.
        """
        for lead_source in self.leads_sources:
            if lead_source.city == city:
                return lead_source
        return None

    def get_all_cities(self) -> List[str]:
        """
        Get all cities from the lead sources
        :return: A list of cities
        """
        return [lead_source.city for lead_source in self.leads_sources]
