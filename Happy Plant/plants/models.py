from django.db import models
from users.models import User
from django import forms
from django.utils import timezone

class PlantType(models.Model): #just plant types
    latin_name = models.CharField(max_length=255)
    family = models.CharField(max_length=255)
    common_name = models.JSONField(default=list) 
    category = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    climate = models.CharField(max_length=255)
    temp_max = models.JSONField(default=dict) 
    temp_min = models.JSONField(default=dict) 
    ideal_light = models.CharField(max_length=255)
    tolerated_light = models.CharField(max_length=255)
    watering = models.CharField(max_length=255)
    insects = models.JSONField(default=list)  
    diseases = models.CharField(max_length=255)
    use = models.JSONField(default=list) 

    def __str__(self):
        return f'{self.common_name}'

class Plant(models.Model): #user's plant
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant_type = models.ForeignKey(PlantType, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    age = models.IntegerField()
    last_watered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.species})"


class PlantForm(forms.ModelForm): #form for fill
    class Meta:
        model = Plant
        fields = ['name', 'plant_type', 'species', 'age']
