from abc import ABC, abstractmethod
from typing import List

from property import ForSaleProperty


class LeadsFilter(ABC):

    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def apply_filter(self, leads: List[ForSaleProperty]) -> List[ForSaleProperty]:
        pass
