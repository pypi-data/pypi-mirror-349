from typing import List

from flows.leads_generator_flow.leads_filters.abstract_filter import LeadsFilter
from flows.leads_generator_flow.leads_filters.ap_filter import ASKING_PRICE_FILTER
from flows.leads_generator_flow.leads_filters.bedrooms_filter import BEDROOMS_FILTER
from flows.leads_generator_flow.leads_filters.internal_neighborhoods_filter import IN_CITY_NEIGHBORHOODS_FILTER
from flows.leads_generator_flow.leads_filters.property_sqft_filter import SQFT_FILTER

leads_filters: List[LeadsFilter] = [
    IN_CITY_NEIGHBORHOODS_FILTER, # Has to be the first filter
    ASKING_PRICE_FILTER,
    BEDROOMS_FILTER,
    SQFT_FILTER
]
