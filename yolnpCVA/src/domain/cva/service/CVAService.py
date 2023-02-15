
from src.infrastructure.computer_vision.yolnp_infer import ConfigFile, YOLNP
from src.domain.plate.service.PlateService import PlateService
from src.infrastructure.cva.model import CVAModel
from src.exceptions.cva import VideoNotValid
from os import remove as remove_file
from dataclasses import asdict
from src.utils import utils
from os import makedirs
from io import BytesIO
from glob import glob
from os import path
import yaml
import cv2

class CVAService:
    def __init__(self) -> None:
        self.plate_service = PlateService()
        self.threads_folder = path.join(self.plate_service.get_storage_dir(),'threads')
        [remove_file(thread_file) for thread_file in glob(path.join(self.threads_folder,'*.yaml'))]

    def get_stream(self,camera_id):
        while True:
            if not self.is_thread_exist_by_id(camera_id):
                frame = cv2.imread(path.join(
                                            'storage',
                                            'resource',
                                            'stopped.jpg'
                                        ),)

                ret, buffer = cv2.imencode('.jpg',frame)
                frame = buffer.tobytes()
                
                return (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            try:
                frame = cv2.imread(path.join(
                            self.plate_service.get_frame_path(camera_id),
                            'frame.jpg'
                        ),)

                ret, buffer = cv2.imencode('.jpg',frame)
                frame = buffer.tobytes()
                
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except:
                frame = cv2.imread(path.join(
                                            'storage',
                                            'resource',
                                            'stopped.jpg'
                                        ),)

                ret, buffer = cv2.imencode('.jpg',frame)
                frame = buffer.tobytes()
                
                return (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')                

    def get_mini(self,camera_id):
        try:
            with open(
                    path.join(
                        self.plate_service.get_frame_path(camera_id),
                        'frame.jpg'
                    ),
                'rb'
            ) as fh:
                buff = BytesIO(fh.read())

                return (200,(buff,f'image/jpeg',f"{'frame'}.jpeg"))

        except FileNotFoundError : return (500,{'status': 'File Not Found'})
        except Exception as e : return (500,{'status': str(e)})
        
    def start_cva_service(self,data: CVAModel) -> None:
        filepath = self.create_thread_file(data)
        if not filepath: return

        try: makedirs(self.plate_service.get_camera_path(data.camera_id)) #to save locally
        except FileExistsError: pass
        except Exception as e: raise(e)

        configuration = ConfigFile(filepath)
        configuration.activate_running(True)

        utils.r(f"/camera/{str(data.camera_id)}/",utils.Methods.PATCH,data={"active":True})
        try:
            YOLNP(USER_FILE=configuration,SHOW=False).run(True) #Start run the alpr
        except:
            utils.r(f"/camera/{str(data.camera_id)}/",utils.Methods.PATCH,data={"active":False})
        finally:
            utils.r(f"/camera/{str(data.camera_id)}/",utils.Methods.PATCH,data={"active":False})
            

    def stop_cva_service(self,camera_id: str) -> None:
        threads = glob(path.join(self.threads_folder,'*.yaml'))
        for thread in threads:
            if camera_id in thread.split("\\")[-1]: 
                ConfigFile(thread).deactivate_running(True)
                break
    
    def get_dir_thread_file(self,data:CVAModel) -> str: return path.join(self.threads_folder,f'{data.camera_id}.yaml')
    def get_dir_thread_file_by_id(self,camera_id:str) -> str: return path.join(self.threads_folder,f'{camera_id}.yaml')


    def is_thread(self,data: CVAModel) -> bool:
        _dir = self.get_dir_thread_file(data)
        if path.isfile(_dir): return False
        return _dir

    def is_thread_exist_by_id(self,camera_id: str) -> bool:
        _dir = self.get_dir_thread_file_by_id(camera_id)
        return path.isfile(_dir)

    def create_thread_file(self,data: CVAModel) -> bool:
        _dir = self.get_dir_thread_file(data)

        if path.isfile(_dir): return False

        _data = {
            'User': asdict(data),
            'Thread': {
                'Running': False
            }
        }

        with open(_dir,'w') as f:
            yaml.dump(_data, f)

        return _dir