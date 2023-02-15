from src.infrastructure.computer_vision.utils.general import non_max_suppression, scale_coords, letterbox
from src.infrastructure.computer_vision.models.experimental import attempt_load
from src.infrastructure.computer_vision.utils.torch_utils import select_device
from src.infrastructure.computer_vision.models.deep_sort import nn_matching
from src.infrastructure.computer_vision.models.ocr import Detector
from src.infrastructure.computer_vision.utils.plate_tools import *
from src.infrastructure.computer_vision.models.sort import Sort
from src.infrastructure.computer_vision.utils import ConfigFile
from src.infrastructure.plate.model import Plate as PlateModel
from src.domain.plate.service.PlateService import PlateService
from src.infrastructure.computer_vision import models
from src.exceptions.cva import VideoNotValid
from typing import List, Tuple
from datetime import datetime
from uuid import uuid4
from os import path, mkdir
import numpy as np
import random
import torch
import time
import cv2
import sys

class YOLNP:
    def __init__(self, USER_FILE: ConfigFile ,CONFIG_FILE: ConfigFile = ConfigFile("src/config/YOLNP_Config.yaml"), SHOW=True) -> None: 
        sys.modules['models'] = models
        self.param: ConfigFile = CONFIG_FILE
        self.user_param: ConfigFile = USER_FILE
        self.__IMSHOW = SHOW
        self.detector = Detector()
        self.plate_service = PlateService()
        self.platesManagementSession = PlateRecognization(self.param.config_from('PaddleOCR')['repeat_define_rec'])

    def run(self,make_draw=False) -> None:
        METRIC = nn_matching.NearestNeighborDistanceMetric(
                "cosine",
                self.param.config_from('DeepSortModelConfig')['max_cosine_distance'],
                self.param.config_from('DeepSortModelConfig')['nn_budget']
        )

        model_config = self.param.config_from('Yolo7ModelConfig')

        deepsortTracker = Sort(max_age=5,
                       min_hits=2,
                       iou_threshold=0.2) 

        VIDEO_PATH = self.user_param.config_from("User")['camera_source']

        modelInfer = attempt_load(
                model_config['path'].replace("\\","/"),
                map_location=self.param.config_from('Env')['device']
        ) 
        
        try:
            cameraVideoContent = cv2.VideoCapture(VIDEO_PATH)
        except:
            self.user_param.destruct()
        if cameraVideoContent.read() == (False,None):
            self.user_param.destruct()
            raise VideoNotValid()

        videoFPS = float(self.user_param.config_from("User")['camera_fps'])
        
        framesProccessed = 0

        #pegar qntos frames meus crops aparecem e dividir pelo framerate do video

        device = select_device(self.param.config_from('Env')['device'])

        colors = [[random.randint(0, 255) for _ in range(3)] for _ in model_config['classes']]
    
        # while video is running
        processCamera = True
        prev_frame_time = 0 
        new_frame_time = 0
        
        dn = datetime.now().isoformat().replace(":","").replace(".","")
        while self.user_param.is_active() and processCamera: #If the condition is equal to false, alpr stops
            self.user_param.reload()

            plates: List[Tuple] = []
            framesProccessed += 1
            isVideoValid, frame = cameraVideoContent.read()
            # frame = cv2.rotate(frame, cv2.ROTATE_180) #old bug '-'

            if isVideoValid: npImgArray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else: break

            img = letterbox(npImgArray, model_config['data_size_infer'], stride=32)[0]

            # Convert
            img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
            img = np.ascontiguousarray(img)

            img = torch.from_numpy(img).to(device).float() / 255

            if img.ndimension() == 3: img = img.unsqueeze(0)
            
            # Make predictions

            pred = modelInfer(img)[0]
            pred = non_max_suppression(pred,
                model_config['config_thresh'],
                model_config['config_iou_thresh'],
                classes=[i for i in range(len(model_config['classes']))],
                agnostic=model_config['nms_max_overlap']
            )

            for det in pred:  # detections per image
                if not len(det): continue
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()

                dets_to_sort = np.empty((0,6))
                # NOTE: We send in detected object class too
                for x1,y1,x2,y2,conf,detclass in det.cpu().detach().numpy():
                    dets_to_sort = np.vstack((dets_to_sort, 
                                np.array([x1, y1, x2, y2, conf, detclass])))     
            
                    tracked_dets = deepsortTracker.update(dets_to_sort,1)

                    # draw boxes for visualization
                    if len(tracked_dets)>0:

                        bbox_xyxy = tracked_dets[:,:4]
                        identities = tracked_dets[:, 8]
                        categories = tracked_dets[:, 4]
                        confidences = dets_to_sort[:, 4]
                        
                        for box, id, cat, acc in zip(bbox_xyxy,identities,categories,confidences):
                            id = str(int(id)) + "__" + dn
                            x1, y1, x2, y2 = [int(i) for i in box]
                            crop_plate = frame[y1:y2,x1:x2]
                            try: plate_content = self.__plate_rec(crop_plate)
                            except Exception as e: print(e); continue
                            self.platesManagementSession.register_plate_det(str(id),plate_content)
                            plate_content = self.platesManagementSession.get_plate(str(id))

                            plate_name_id = str(uuid4())
                            # ok, if u wanna understand it, pay attention to this "plates variable", see more in next comment
                            plates.append(
                                (
                                    PlateModel(
                                        tracking_id=str(id),
                                        camera_id=self.user_param.config_from('User')['camera_id'],
                                        image_id=plate_name_id,
                                        content=plate_content,
                                        duration= None,
                                        in_frames=1,
                                        datetime=datetime.now().isoformat()
                                    ),
                                    crop_plate                                       
                                )
                            )

                            if make_draw: frame = self.__draw_boxes(frame, box, id, cat, acc, model_config['classes'], colors,plate_content)
           
            content_plate_list_local: List[str] = []

            new_frame_time = time.time()
            fps = "{:.2f}".format(float(1/(new_frame_time-prev_frame_time)))
            prev_frame_time = new_frame_time            

            #each while loop, plates is reseted, so now, what we have in this variable is basically the plates got in this frame
            #this for loop is inside while loop ok?
            #with this informations, here is where we apply our business logic
            #feel free to debug it or just print all variables
            for plate_info in plates:
                plate = plate_info[0]
                plate_crop = plate_info[1]
                if plate.content not in content_plate_list_local and plate.content != None:
                    content_plate_list_local.append(plate.content)
                    plate_in_db = self.plate_service.get_plate_by_tracking(plate.tracking_id)
                    
                    if not plate_in_db:
                        self.plate_service.insert_plate_in_db(plate,self.user_param.config_from('User')['camera_id'])
                        r = str(uuid4()) + ".jpg"
                        cv2.imwrite(r,plate_crop)          
                        self.plate_service.update_plate_image(plate,r)
                    
                    if self.plate_service.get_plate_by_tracking(plate.tracking_id)['content'] != plate.content:
                        self.plate_service.update_plate_content_by_tracking_id(plate)
                        r = str(uuid4()) + ".jpg"
                        cv2.imwrite(r,plate_crop)          
                        self.plate_service.update_plate_image(plate,r)
             
                    # plate.duration = (totalFrames / videoFPS) - ((totalFrames - self.plate_service.get_plate_by_tracking(plate.tracking_id)[0]['in_frames']) / videoFPS)
                    
                    plate.duration = 0
                    self.plate_service.update_plate_in_frames(plate)
                    self.plate_service.update_plate_duration(plate)



            if self.__IMSHOW:
                image_h, image_w, _ = frame.shape
                scale_percent = 50
                width = int(image_w * scale_percent / 100)
                height = int(image_h * scale_percent / 100)
                dim = (width,height)
                image_copy = cv2.resize(frame.copy(),dim)                                    
                cv2.putText(image_copy, "FPS: "+fps, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow("",image_copy)
                k = cv2.waitKey(33)
                if k==27: processCamera = False

            try:
                mkdir(self.plate_service.get_frame_path(self.user_param.config_from('User')['camera_id']))
            except: pass

            cv2.imwrite(path.join(
                    self.plate_service.get_frame_path(self.user_param.config_from('User')['camera_id']),
                    'frame.jpg'
                ),frame)

        self.user_param.destruct()

    def __plate_rec(self,crop_plate):
        rescaled = cv2.resize(
            crop_plate, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC
        )
        grayscale = cv2.cvtColor(rescaled, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((1, 1), np.uint8)
        dilated = cv2.dilate(grayscale, kernel, iterations=1)
        eroded = cv2.erode(dilated, kernel, iterations=1)
        sharpened = YOLNP.__unsharp_mask(eroded)         
        text_image_content = self.detector.paddle_ocr(sharpened)   #ocr happens here, look <--          

        return text_image_content
    
    def __draw_boxes(self,img, box, identities, categories=None, confidences = None, names=None, colors = None,treated_content=str):
        x1, y1, x2, y2 = [int(i) for i in box]
        #i would be very happy if u could make this work
        tl = 2 or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness

        cat = int(categories) if categories is not None else 0
        # conf = confidences[i] if confidences is not None else 0

        color = colors[cat]
        
        cv2.rectangle(img, (x1, y1), (x2, y2), color, tl)

        label = f"{treated_content}"
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = x1 + t_size[0], y1 - t_size[1] - 3
        cv2.rectangle(img, (x1, y1), c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (x1, y1 - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

        return img

    @staticmethod
    def __unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=2.0, threshold=0):
        blurred = cv2.GaussianBlur(image, kernel_size, sigma)
        sharpened = float(amount + 1) * image - float(amount) * blurred
        sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
        sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
        sharpened = sharpened.round().astype(np.uint8)
        if threshold > 0:
            low_contrast_mask = np.absolute(image - blurred) < threshold
            np.copyto(sharpened, image, where=low_contrast_mask)
        return sharpened     