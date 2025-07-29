from typing import List

from flows.leads_generator_flow.leads_filters.abstract_filter import LeadsFilter
from property import ForSaleProperty


class OutsideCityNeighborhoodFilter(LeadsFilter):
    """
    White list of neighborhoods
    """

    def __init__(self, white_list_neighborhoods: List[str]):
        super().__init__('Neighborhoods Filter')
        self.white_list_neighborhoods: List[str] = white_list_neighborhoods

    def apply_filter(self, leads: List[ForSaleProperty]) -> List[ForSaleProperty]:
        return [lead for lead in leads if lead.address.city in self.white_list_neighborhoods]


OUTSIDE_NEIGHBORHOODS_FILTER: OutsideCityNeighborhoodFilter = OutsideCityNeighborhoodFilter(
    white_list_neighborhoods=[
        "Pittsburgh", "Monroeville", "Dormont", "Castle Shannon", "Whitehall", "Brentwood",
        "Baldwin", "Mt. Lebanon", "Carnegie", "Scott Township", "MT Washington", "Bethel Park",
        "Greentree", "Crafton", "Avalon", "Bellevue", "Swissvale"
    ]
)
