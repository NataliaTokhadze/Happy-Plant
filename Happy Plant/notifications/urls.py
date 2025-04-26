from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from notifications.views import (NotificationViewSet)

router = routers.DefaultRouter()
router.register('notifications', NotificationViewSet, basename='urls')


urlpatterns = [
    path('', include(router.urls)),
]  