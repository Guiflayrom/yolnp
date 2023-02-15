from django.contrib import admin
from django.urls import path,include
from apps.accounts.views import GroupsView, PermissionsView, UserViewSet, LogoutView
from apps.camera.views import CameraViewSet, DashboardView, StreamView, ThumbnailView, StopCVAView, StartCVAView, ResetDBView
from apps.plate.views import PlateViewSet, AlertViewSet, DisplayImage
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

schema = swagger_get_schema_view(
    openapi.Info(
        title='YOLNP (You Only Look Once) Swagger',
        default_version='1.0.0',
        description="A swagger for a YOLNP"
    ),
    public=True,
)

router = routers.SimpleRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'camera', CameraViewSet, basename='camera')
router.register(r'alert', AlertViewSet, basename='alert')
router.register(r'plate',PlateViewSet,basename='plate')

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        'api/v1/',
        include(
            [
                path(r'', include(router.urls)),
                path(r'group/',GroupsView.as_view()),
                path(r'permission/',PermissionsView.as_view()),
                
                path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                path('logout/',LogoutView.as_view(), name='logout'),
                
                path('dashboard/<uuid:pk>/',DashboardView.as_view(),name="dashboard"),
                path('dashboard/<uuid:pk>/delete/',ResetDBView.as_view(),name='resetDB'),
                
                path('cva/start/',StartCVAView.as_view(),name='cva_start'),
                path('cva/stop/<str:camera_id>/',StopCVAView.as_view(),name='cva_stop'),
                path('cva/camera/<str:camera_id>/thumbnail/',ThumbnailView.as_view(),name='cva_thumbnail'),
                path('cva/camera/<str:camera_id>/stream/',StreamView,name='cva_stream'),
                
                path('image/<str:camera>/<str:plate>/',DisplayImage.as_view(),name="plate_images"),
                
                path('',schema.with_ui('swagger',cache_timeout=0)),
                path('swagger/',schema.with_ui('swagger',cache_timeout=0)),
                path('redoc/',schema.with_ui('redoc',cache_timeout=0)),
            ]
        )
    )
]
