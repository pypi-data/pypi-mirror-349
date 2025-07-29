from typing import List

from flows.leads_generator_flow.leads_filters.abstract_filter import LeadsFilter
from property import ForSaleProperty


class AskingPriceFilter(LeadsFilter):
    """
    White list of neighborhoods
    """

    def __init__(self, min_price: int, max_price: int):
        super().__init__('Asking Price Filter')
        self.min_price: int = min_price
        self.max_price: int = max_price

    def apply_filter(self, leads: List[ForSaleProperty]) -> List[ForSaleProperty]:
        return [lead for lead in leads if self.min_price <= lead.asking_price <= self.max_price]


ASKING_PRICE_FILTER: AskingPriceFilter = AskingPriceFilter(
    min_price=80000,  # 80K
    max_price=210000  # 210K
)
