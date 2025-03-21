from django.contrib import admin
from .models import PlantType, Plant

admin.site.register(PlantType)

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'plant_type', 'age', 'last_watered')
    search_fields = ('name', 'species', 'plant_type__name')
    list_filter = ('plant_type', 'user')
