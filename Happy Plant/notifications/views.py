from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

class NotificationViewSet(ViewSet, ListModelMixin):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return render(request, 'notifications/notifications.html')
