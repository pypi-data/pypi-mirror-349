from abc import ABC, abstractmethod
from typing import Optional

from api import EnergyData


class Handler(ABC):
    def __init__(self) -> None:
        self.data: Optional[EnergyData] = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @abstractmethod
    def handle(self, data: EnergyData) -> None:
        pass
