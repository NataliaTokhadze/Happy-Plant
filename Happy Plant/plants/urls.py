from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlantViewSet, PlantTypeViewSet

router = DefaultRouter()
router.register('plants', PlantViewSet, basename='plants')
router.register('plant-types', PlantTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
