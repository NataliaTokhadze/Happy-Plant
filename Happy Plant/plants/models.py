from django.db import models
from users.models import User
from django import forms
from django.utils import timezone

class PlantType(models.Model):
    scientific_name = models.CharField(max_length=100)
    family = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.scientific_name

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
