from django.core.management.base import BaseCommand
from users.models import User
from notifications.firebase_service import send_push_notification
import requests

class Command(BaseCommand):
    help = 'Send daily notifications to users about plant care and bad weather.'

    def handle(self, *args, **kwargs):
        users = User.objects.all()

        for user in users:
            if not user.device_token:
                continue

            # Допустим, в модели User есть location (например: "Tbilisi, Georgia")
            location = getattr(user, 'location', None)
            if not location:
                continue

            # Получаем погоду
            weather_data = self.get_weather_data(location)

            if not weather_data:
                continue

            condition = weather_data.get('current', {}).get('condition', '').lower()

            if self.is_bad_weather(condition):
                send_push_notification(
                    device_token=user.device_token,
                    title="🌧️ Bad Weather Warning!",
                    body=f"Today: {condition}. Protect your plants!"
                )
            else:
                send_push_notification(
                    device_token=user.device_token,
                    title="🌱 Daily Reminder",
                    body="Don't forget to water your plants today!"
                )

    def get_weather_data(self, location):
        url = "https://yahoo-weather5.p.rapidapi.com/weather"
        querystring = {
            "location": location,
            "format": "json",
            "u": "c"
        }
        headers = {
            "x-rapidapi-key": "e4dae51515msh6f838bf6e9f69c1p1b221ejsn91ee8b271ba6",
            "x-rapidapi-host": "yahoo-weather5.p.rapidapi.com"
        }
        try:
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            return {
                "current": {
                    "condition": data.get("current_observation", {}).get("condition", {}).get("text")
                }
            }
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return None

    def is_bad_weather(self, condition):
        bad_conditions = ['rain', 'storm', 'snow', 'hail', 'thunder']
        return any(bad in condition for bad in bad_conditions)
