from src.domain.plate.interface import PlateInterface
from src.infrastructure.plate.model import Plate
from dataclasses import asdict
from typing import Tuple, AnyStr
from dotenv import load_dotenv
from os import getenv
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.results import InsertOneResult
from pymongo.cursor import Cursor

class MongoDBPlateRepository(PlateInterface):
    def __init__(self) -> None:
        load_dotenv()
        self.db = MongoClient(getenv('MONGO_URL_CONNECTION'))
        super().__init__()
                                                                                      
    def create(self, plate: Plate, base: Tuple[str]) -> InsertOneResult: return self.db[base[0]][base[1]].insert_one(asdict(plate))
        
    def get(self, id: AnyStr, base: Tuple[str]) -> dict: return self.db[base[0]][base[1]].find_one({'_id': ObjectId(id)})

    def put(self, id: str or ObjectId, plate: Plate, base: Tuple[str]) -> dict: return self.db[base[0]][base[1]].find_one_and_replace({'_id': ObjectId(id)},asdict(plate)) if type(id) == str else self.db[base[0]][base[1]].find_one_and_replace({'_id': id},asdict(plate))

    def delete(self, id: str or ObjectId, base: Tuple[str]) -> dict: return self.db[base[0]][base[1]].find_one_and_delete({'_id': ObjectId(id)}) if type(id) == str else self.db[base[0]][base[1]].find_one_and_delete({'_id': id})

    def fetch(self, query: dict, base: Tuple[str]) -> Cursor: return self.db[base[0]][base[1]].find(query)

    def get_all(self, base: Tuple[str]) -> Cursor: return self.fetch({}, base)

    def update_one(self, query: dict, new_values: dict, base: Tuple[str]): self.db[base[0]][base[1]].update_one(query, new_values)