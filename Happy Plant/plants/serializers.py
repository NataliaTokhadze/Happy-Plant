from rest_framework import serializers
from .models import Plant, PlantType

class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantType
        fields = [
            'latin_name', 'family', 'common_name', 'category', 'origin', 'climate',
            'temp_max', 'temp_min', 'ideal_light', 'tolerated_light', 'watering', 
            'insects', 'diseases', 'use'
        ]

class PlantSerializer(serializers.ModelSerializer): # მომხმარებლის მცენარეებისთვის
    plant_type = PlantTypeSerializer(read_only=True)

    class Meta:
        model = Plant
        fields = ['id', 'name', 'plant_type', 'species', 'age', 'last_watered']
    
    def create(self, validated_data):
        plant_type_data = validated_data.pop('plant_type', None)
        plant = Plant.objects.create(**validated_data)
        if plant_type_data:
            plant.plant_type = plant_type_data
            plant.save()
        return plant

