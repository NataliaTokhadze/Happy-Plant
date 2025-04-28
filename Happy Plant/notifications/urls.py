from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceTokenViewSet

router = DefaultRouter()
router.register('device-tokens', DeviceTokenViewSet, basename='device-tokens')

urlpatterns = [
    path('', include(router.urls)),
]
