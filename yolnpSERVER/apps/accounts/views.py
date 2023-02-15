import json
from django.http import HttpResponse
from rest_framework import generics
from django.contrib.auth.models import Group, Permission
from .serializers import GroupSerializer
from rest_framework import status

from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated


class LogoutView(APIView):
    serializer_class = TokenRefreshSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        if request.method == 'POST':
            self.permission_classes = []
        return request    

class PermissionsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    def get(self,request) -> HttpResponse:
        return HttpResponse(
            json.dumps(
                [
                    {
                        'id':permission.id,
                        'name': permission.name,
                        'codename': permission.codename
                    }
                    for permission in Permission.objects.filter(codename__contains="uc_")
                ]
            ),
            content_type='application/json'
        )

class GroupsView(generics.ListAPIView):

    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self,request) -> HttpResponse:
        return HttpResponse(
            json.dumps(
                [
                    {
                        'id': group.id,
                        'name': group.name,
                        'permissions': [
                            {
                                'id':permission.id,
                                'name': permission.name,
                                'codename': permission.codename
                            }
                        for permission in group.permissions.all()
                        ]
                    }
                    for group in Group.objects.all()
                ]
            ),
            content_type="application/json",
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
