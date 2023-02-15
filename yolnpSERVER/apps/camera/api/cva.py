from .utils import r, Methods
from dotenv import load_dotenv
from requests import Response
from os import getenv
from django.shortcuts import render


class CVA:
    def __init__(self) -> None:
        load_dotenv()
        self.host = getenv('CVA_HOST')
        self.key = {'X-API-Key': getenv('API_AUTHORIZATION_KEY')}
    
    def request_start(self,data:dict) -> Response: return r(self.host, 'cva/start', Methods.POST, data=data, headers=self.key)
    def request_stop(self,camera_id:str) -> Response: return r(self.host, f'cva/stop/{camera_id}', Methods.GET, headers=self.key)
    def request_thumbnail(self,camera_id:str) -> Response: return r(self.host, f'cva/camera/{camera_id}/thumbnail', Methods.GET, headers=self.key)
    def request_stream(self,request,camera_id:str) -> Response: return render(request,"stream.html",{"stream_url":f'{self.host}/cva/camera/{camera_id}/stream/'})
    

