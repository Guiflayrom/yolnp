from rest_framework import serializers
from .models import Camera
from apps.plate.serializer import PlateSerializer, AlertSerializer


class CameraSerializer(serializers.ModelSerializer):
    alert = AlertSerializer(many=True,read_only=True)
    plate = PlateSerializer(many=True,read_only=True)
    
    class Meta:
        model = Camera
        fields = ('id','name','rtsp','active','alert_stolen_cars','fps','user','alert','plate')