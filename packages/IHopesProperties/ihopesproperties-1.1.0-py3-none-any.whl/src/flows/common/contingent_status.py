from enum import Enum

class ContingentStatus(Enum):
    UNDER_CONTRACT = "Under Contract"
    FOR_SALE = "For Sale"
    RECENTLY_SOLD = "Recently Sold"
    OFF_MARKET = "Off Market"