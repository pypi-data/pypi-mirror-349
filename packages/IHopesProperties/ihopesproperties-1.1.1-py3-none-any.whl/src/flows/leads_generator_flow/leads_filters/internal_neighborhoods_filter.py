from typing import List

from flows.leads_generator_flow.leads_filters.abstract_filter import LeadsFilter
from property import ForSaleProperty


BEECHVIEW = ["15216"]
BROOKLINE = ["15226"]
MOUNT_WASHINGTON = ["15211"]
BRIGHTON_HEIGHTS = ["15212"]
GREENFIELD = ["15217"]
BLOOMFIELD = ["15224"]
SQUIRREL_HILL = ["15217"]
CASTLE_SHANNON = ["15234"]
DORMONT = ["15216"]
BRENWOOD = ["15227"]
MT_LEBANON = ["15228"]
MT_WASHINGTON = ["15211"]
GREEN_TREE = ["15242", "15220", "15205"]
SWISSVALE = ["15218", "15120"]


class InCityNeighborhoodsFilter(LeadsFilter):
    """
    White list of inside Pittsburgh neighborhoods
    """

    def __init__(self, in_city_zip_codes: List[List[int]]):
        super().__init__('In City Neighborhoods Filter')
        # Flatten the list of lists
        self.in_city_zip_codes: List[int] = [zip_code for zip_codes in in_city_zip_codes for zip_code in zip_codes]

    def apply_filter(self, leads: List[ForSaleProperty]) -> List[ForSaleProperty]:
        """
        Property should pass this filter if it's in the city of Pittsburgh in one of the specified zip codes or if it's
        just outside the city limits (already filtered the desired outside-Pittsburgh neighborhoods)
        :param leads:
        :return:
        """
        def is_in_city(lead: ForSaleProperty) -> bool:
            """
            If the property is in the city of Pittsburgh and in one of the specified zip codes,
             or - if it's just outside the city limits.
            :param lead:
            :return:
            """
            in_pittsburgh: bool = lead.address.city == 'Pittsburgh'
            in_city_zip_code: bool = lead.address.zip_code in self.in_city_zip_codes
            return (in_pittsburgh and in_city_zip_code) or not in_pittsburgh

        in_city_leads: List[ForSaleProperty] = [lead for lead in leads if is_in_city(lead)]

        return in_city_leads


IN_CITY_NEIGHBORHOODS_FILTER: InCityNeighborhoodsFilter = InCityNeighborhoodsFilter(
    in_city_zip_codes=[
        BEECHVIEW,
        BROOKLINE,
        MOUNT_WASHINGTON,
        BRIGHTON_HEIGHTS,
        GREENFIELD,
        BLOOMFIELD,
        SQUIRREL_HILL,
        CASTLE_SHANNON,
        DORMONT,
        BRENWOOD,
        MT_LEBANON,
        MT_WASHINGTON,
        GREEN_TREE,
        SWISSVALE
    ]
)
