from django.db import models
from users.models import User
from django import forms
from django.utils import timezone

class PlantType(models.Model):
    latin_name = models.CharField(max_length=255)
    family = models.CharField(max_length=255)
    common_name = models.JSONField(default=list)  # Используем JSONField для списка
    category = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    climate = models.CharField(max_length=255)
    temp_max = models.JSONField(default=dict)  # Используем JSONField для словаря
    temp_min = models.JSONField(default=dict)  # Используем JSONField для словаря
    ideal_light = models.CharField(max_length=255)
    tolerated_light = models.CharField(max_length=255)
    watering = models.CharField(max_length=255)
    insects = models.JSONField(default=list)  # Используем JSONField для списка
    diseases = models.CharField(max_length=255)
    use = models.JSONField(default=list) 

    def __str__(self):
        return f'{self.common_name}'

class Plant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant_type = models.ForeignKey(PlantType, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    age = models.IntegerField()
    last_watered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.species})"


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'plant_type', 'species', 'age']
