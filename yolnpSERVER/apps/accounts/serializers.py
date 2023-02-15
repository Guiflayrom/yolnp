from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from .models import User
from apps.camera.serializer import CameraSerializer

class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ('id','name','codename')


class GroupSerializer(serializers.ModelSerializer):

    permissions = PermissionSerializer(many=True,read_only=True)

    class Meta:
        model = Group
        fields = ("id","name","permissions")


class UserSerializer(serializers.ModelSerializer):

    groups = GroupSerializer(many=True,read_only=True)
    camera = CameraSerializer(many=True,read_only=False)

    class Meta:
        model = User
        fields = ("id",'date_joined','username','email','groups','camera')

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['email']
            )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self,instance,validated_data):
        print(validated_data)
        user = User.objects.get(email=validated_data['email'])
        user.email = validated_data['email']
        user.username = validated_data['email']
          
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    