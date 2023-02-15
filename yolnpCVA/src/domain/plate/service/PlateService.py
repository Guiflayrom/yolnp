from src.domain.plate.interface.PlateInterface import PlateInterface
from src.infrastructure.plate.model import Plate
from os import remove as remove_file
from shutil import rmtree
from typing import AnyStr
from io import BytesIO
from os import path
import inject
from src.utils import utils
import base64
from os import getenv
import requests

class PlateService:
    @inject.autoparams()
    def __init__(self, plate_repository: PlateInterface = PlateInterface) -> None: 
        self.__repository = plate_repository
        self.__default_db = ('Yolnp','PlateDB')
        self.__storage_dir = 'storage'
        self.__default_image_extension = "jpg"

    def get_default_image_extension(self,with_point: bool = False): return self.__default_image_extension if with_point == False else "." + self.__default_image_extension

    def get_storage_dir(self) -> str: return self.__storage_dir

    def get_camera_path(self, camera_id:str) -> str: return path.join(self.__storage_dir,'cameras',camera_id) + "\\"

    def get_frame_path(self, camera_id:str) -> str: return self.get_camera_path(camera_id) + "frame"

    def get_plate_by_tracking(self,tracking_id: str) -> list: 
        r = utils.r(f'plate/{tracking_id}/',utils.Methods.GET)
        if r.status_code == 200: return r.json()
        else: return {}
        
    
    def insert_plate_in_db(self,plate: Plate, camera_id: str) -> None: 
        payload = {'id':plate.tracking_id,'content':plate.content,'duration':plate.duration,'in_frames':plate.in_frames,'camera':camera_id}
        r = utils.r(f'plate/',utils.Methods.POST,data=payload)
    
    def update_plate_in_frames(self, plate: Plate): 
        res = self.get_plate_by_tracking(plate.tracking_id)
        if res:
            n = int(res['in_frames']) + 1
            payload = {'in_frames':n}
            r = utils.r(f'plate/{plate.tracking_id}/',utils.Methods.PATCH,data=payload)
        
        
    def update_plate_duration(self,plate: Plate) -> None: 
        payload = {'duration':plate.duration}
        r = utils.r(f'plate/{plate.tracking_id}/',utils.Methods.PATCH,data=payload)

    def update_plate_image(self,plate: Plate,image:str) -> None: 
        r = requests.patch(getenv('SERVER_HOST') + f'plate/{plate.tracking_id}/',files={'image':open(image,'rb')})
        remove_file(
            image
        )

    def update_plate_content_by_tracking_id(self,plate: Plate) -> None: 
        payload = {'content':plate.content}
        r = utils.r(f'plate/{plate.tracking_id}/',utils.Methods.PATCH,data=payload)
        