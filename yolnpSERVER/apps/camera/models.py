from django.db import models
from uuid import uuid4
from django.core.validators import RegexValidator
from apps.accounts.models import User

class Camera(models.Model):
    rtsp_validator = RegexValidator(
        regex='(rtsp|rtmp):\/\/?([a-zA-Z0-9:@./_]*)',
        message='Format must be rtsp:// [...]'
    )

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)
    name = models.CharField(max_length=255,null=False,blank=False)
    rtsp = models.CharField(max_length=255,null=False,blank=False)
    active = models.BooleanField(default=False)
    alert_stolen_cars = models.BooleanField(default=False)
    fps = models.FloatField(null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='camera')


    def __str__(self) -> str:
        return self.name