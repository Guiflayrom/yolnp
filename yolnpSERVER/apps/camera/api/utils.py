import requests
from requests import Response
import json


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

def r(host:str,endpoint:str,method:str,data={},headers={}) -> Response:
    url = vj(host,endpoint)

    headers = {'Content-Type':'application/json',**headers}
    
    if method.upper() == Methods.GET: return requests.get(url,headers=headers)
    elif method.upper() == Methods.PUT: return requests.put(url,headers=headers,data=json.dumps(data))
    elif method.upper() == Methods.POST: return requests.post(url,headers=headers,data=json.dumps(data))
    elif method.upper() == Methods.PATCH: return requests.patch(url,headers=headers,data=json.dumps(data))
    elif method.upper() == Methods.DELETE: return requests.delete(url,headers=headers)
    
    return None