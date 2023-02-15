from os import remove as remove_file
from yaml.loader import SafeLoader
from os import path
import yaml

class ConfigFile:
    def __init__(self,file: str) -> None:
        self.__filename = file
        try: 
            with open(self.__filename) as f: self.__data = yaml.load(f, Loader=SafeLoader)
        except Exception as e: raise e
    
    def config_from(self,key: str) -> dict: return self.__data[key]

    def get_data(self) -> dict: return self.__data

    def activate_running(self,save_state:bool=False) -> None: 
        self.__data['Thread']['Running'] = True
        with open(self.__filename, 'w') as file: yaml.dump(self.__data, file)
        if save_state: self.save_state()

    def deactivate_running(self,save_state:bool=False) -> None: 
        self.__data['Thread']['Running'] = False
        if save_state: self.save_state()

    def save_state(self) -> None: 
        with open(self.__filename, 'w') as file: yaml.dump(self.__data, file)

    def reload(self) -> None:
        try: 
            with open(self.__filename) as f: self.__data = yaml.load(f, Loader=SafeLoader)
        except Exception as e: raise e        

    def is_active(self) -> bool: return self.__data['Thread']['Running']

    def destruct(self) -> None:
        remove_file(self.__filename)
        try:
            cid = self.config_from('User')['camera_id']
            remove_file(
                f'storage/cameras/{ str(cid) }/frame/frame.jpg'
            )
        except:
            pass