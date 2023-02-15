from rest_framework import serializers
from .models import Plate, Alert

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = "__all__"
        
class PlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plate
        fields = "__all__"
        
        
