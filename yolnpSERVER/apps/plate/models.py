from django.db import models
from apps.camera.models import Camera
from uuid import uuid4

def custom_upload_to(instance, filename):
    camera = instance.camera.id
    plate = instance.id
    return 'uploads/{0}/{1}'.format(camera, plate + ".jpg")

class Plate(models.Model):
    id = models.CharField(max_length=255,unique=True,primary_key=True)
    image = models.ImageField(upload_to=custom_upload_to, blank=True,null=True)
    content = models.CharField(max_length=10)
    in_frames = models.IntegerField(default=1,null=True,blank=True)
    duration = models.FloatField(null=True,blank=True)
    detected_at = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=255,blank=True,null=True)
    state = models.CharField(max_length=255,blank=True,null=True)
    camera = models.ForeignKey(Camera,on_delete=models.CASCADE,related_name='plate')

    def __str__(self) -> str:
        return self.content

class Alert(models.Model):
    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)
    plate = models.CharField(max_length=10,null=False,blank=False, unique=True)
    camera = models.ForeignKey(Camera,on_delete=models.CASCADE,related_name='alert')

    def __str__(self) -> str:
        return self.plate