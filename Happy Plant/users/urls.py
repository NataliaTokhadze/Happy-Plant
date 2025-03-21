from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from .views import (UserViewSet, 
                        CreateUserViewSet)

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='urls')
router.register('register', CreateUserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]