from rest_framework.permissions import IsAuthenticated
from .serializer import CameraSerializer
from rest_framework import viewsets
from apps.APIKeyPermission import CustomAPIKeyPermission
from .models import Camera
from apps.plate.models import Plate, Alert
from django.http import HttpResponse
import json
from .api import cva
from collections import Counter
from django.utils import timezone
from .domain.DataAnalist import *

api = cva.CVA()

class StartCVAView(viewsets.generics.ListAPIView):
    permission_classes = (IsAuthenticated,)    
    def post(self,request): 
        res = api.request_start(request.data)
        return HttpResponse(res.content, status=res.status_code)

class StopCVAView(viewsets.generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)    
    def get(self,request,camera_id): 
        res = api.request_stop(camera_id)
        return HttpResponse(res.content, status=res.status_code)

class ThumbnailView(viewsets.generics.ListAPIView):
    permission_classes = (IsAuthenticated,)    

    def get(self,request,camera_id): 
        res = api.request_thumbnail(camera_id)
        if res.status_code == 200: return HttpResponse(res.content, content_type='image/jpeg')
        else: return HttpResponse(status=404)

def StreamView(request,camera_id): return api.request_stream(request,camera_id)

class CameraViewSet(viewsets.ModelViewSet):
    permission_classes = [CustomAPIKeyPermission]
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class ResetDBView(viewsets.generics.ListAPIView):
    permission_classes = (IsAuthenticated,)    
    
    def delete(self,request,pk):
        camera = Camera.objects.get(pk=pk)
        all_plates = Plate.objects.filter(camera=camera)
        for plate in all_plates:
            plate.delete()
        return HttpResponse(status=200)
        
    
class DashboardView(viewsets.generics.ListAPIView):
    permission_classes = (IsAuthenticated,)    
    
    def get(self,request,pk):
        output = {}
        camera = Camera.objects.get(pk=pk)
        five_minutes_ago = timezone.now() - timezone.timedelta(minutes=5)
        
        all_plates = Plate.objects.filter(camera=camera)
        all_alerts = Alert.objects.filter(camera=camera)
        
        pl = [i.content for i in all_plates]
        al = [i.plate for i in all_alerts]
        
        p = Counter(pl)
        a = Counter(al)
        
        intersection = [value for value in pl if value in al]
        intersection_plates_models = []
        for i in intersection:
            for plate in all_plates.filter(content=i):
                intersection_plates_models.append(plate)
                
        output['median_frame'] = get_median_frames(all_plates)
        output['total_plates'] = len(all_plates)
        output['total_alerts'] = sum(p[key] for key in a if key in p)
        output['recurring_plates'] = get_recurring_plates(all_plates)
        output['street_moviment_rate'] = get_street_moviment_rate(all_plates)
        output['street_moviment_list'] = get_street_moviment_list(all_plates.filter(detected_at__gte=five_minutes_ago))
        output['lasted_plates']  = [
            {
                "id":str(plate.id),
                "content":plate.content,
                "detected_at":plate.detected_at.strftime("%d-%m-%Y - %H:%M:%S"),
                "in_frames":plate.in_frames,
                "city":plate.city,
                "state":plate.state,
                "image": f"http://localhost:8000/api/v1/image/{pk}/{plate.id}/"                
            } 
            for plate in all_plates.order_by('-detected_at')]        
        output['alerts'] = [
            {
                "id":str(plate.id),
                "content":plate.content,
                "detected_at":plate.detected_at.strftime("%d-%m-%Y - %H:%M:%S"),
                "in_frames":plate.in_frames,
                "city":plate.city,
                "state":plate.state,
                "image": f"http://localhost:8000/api/v1/image/{pk}/{plate.id}/"
            } for plate in intersection_plates_models]
        
        return HttpResponse(json.dumps(output),headers={'mimetype':'application/json'})
    
