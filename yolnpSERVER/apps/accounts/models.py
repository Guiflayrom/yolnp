from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from uuid import uuid4

class User(AbstractUser):

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)
    username = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)

    class Meta:
        permissions = (
            ("uc_view_dashboard", "Visualizar Dashboard"),
        )


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    position = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='uploads', blank=True)

