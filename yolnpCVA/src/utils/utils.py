import requests
from requests import Response
import json
from os import getenv

class Methods:
    POST = 'POST'
    GET = 'GET'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    
def vj(host:str,endpoint:str):
    if host[-1] == "/": host = host[:-1]
    if endpoint[0] != "/": endpoint = "/"+endpoint
    if endpoint[-1] != "/": endpoint = endpoint + "/"    

    return host + endpoint


def r(endpoint:str,method:str,data={},headers={},files={}) -> Response:
    host = getenv('SERVER_HOST')
    url = vj(host,endpoint)

    if not headers: headers = {'Content-Type':'application/json','Key':getenv('SERVER_KEY'),**headers}
    method = method.upper()
    
    if method == Methods.GET: return requests.get(url,headers=headers)
    elif method == Methods.PUT: return requests.put(url,headers=headers,data=json.dumps(data),files=files)
    elif method == Methods.POST: return requests.post(url,headers=headers,data=json.dumps(data),files=files)
    elif method == Methods.PATCH: return requests.patch(url,headers=headers,data=json.dumps(data),files=files)
    elif method == Methods.DELETE: return requests.delete(url,headers=headers)
    
    return None