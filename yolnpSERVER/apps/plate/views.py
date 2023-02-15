from rest_framework.permissions import IsAuthenticated
from apps.APIKeyPermission import CustomAPIKeyPermission
from .serializer import PlateSerializer,AlertSerializer
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from .models import Plate,Alert
from rest_framework import viewsets, status
from django.http import FileResponse
from rest_framework.response import Response

class AlertViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

class PlateViewSet(viewsets.ModelViewSet):
    # permission_classes = [CustomAPIKeyPermission]
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer

class DisplayImage(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, camera, plate):
        print(camera,plate)
        try:
            img = open(f'uploads/{camera}/{plate}' + '.jpg', 'rb')
            return FileResponse(img)
        except Exception as e:
            print("ERRO:",e)
        return Response(status=404)