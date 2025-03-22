import requests
from plants.models import PlantType

url = "https://house-plants.p.rapidapi.com/all"

headers = {
    "x-rapidapi-key": "e4dae51515msh6f838bf6e9f69c1p1b221ejsn91ee8b271ba6",
    "x-rapidapi-host": "house-plants.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

# Получаем данные из API
plants_data = response.json()

def import_plants_from_api(plants_data):
    for plant in plants_data:
        try:
            # Создаём объект модели PlantType с данными из API
            plant_instance = PlantType.objects.create(
                latin_name=plant['latin'],
                family=plant['family'],
                common_name=plant['common'],
                category=plant['category'],
                origin=plant['origin'],
                climate=plant['climate'],
                temp_max=plant['tempmax'],  # tempmax будет сохранен как словарь
                temp_min=plant['tempmin'],  # tempmin будет сохранен как словарь
                ideal_light=plant['ideallight'],
                tolerated_light=plant['toleratedlight'],
                watering=plant['watering'],
                insects=plant['insects'],
                diseases=plant['diseases'],
                use=plant['use'],
            )
            print(f"Plant {plant['latin']} imported successfully.")
        except Exception as e:
            print(f"Error importing plant {plant['latin']}: {e}")

# Импортируем данные из API
import_plants_from_api(plants_data)
