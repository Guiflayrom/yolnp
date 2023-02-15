from abc import abstractclassmethod, ABC
from typing import List
from src.infrastructure.plate.model import Plate
from typing import AnyStr

class PlateInterface(ABC):
    @abstractclassmethod
    def create(self, Plate: Plate, base: AnyStr) -> dict:
        """"""

    @abstractclassmethod
    def get(self, pk:str, base: AnyStr) -> dict:
        """"""
    
    @abstractclassmethod
    def put(self, pk: str, Plate: Plate, base: AnyStr) -> dict:
        """"""
    
    @abstractclassmethod
    def delete(self, pk: str, base: AnyStr) -> dict:
        """"""
    
    @abstractclassmethod
    def get_all(self, base: AnyStr) -> List[dict]:
        """"""

    @abstractclassmethod
    def fetch(self, query: dict, base: AnyStr) -> List[dict]:
        """"""

    @abstractclassmethod
    def update_one(self, query: dict, base: AnyStr) -> List[dict]:
        """"""