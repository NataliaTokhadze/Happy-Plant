from django.core.management.base import BaseCommand
from users.models import User
from notifications.twilio_service import send_sms_notification
import requests

class Command(BaseCommand):
    help = 'Send daily SMS notifications about plant care and weather'

    def handle(self, *args, **kwargs):
        users = User.objects.all()

        for user in users:
            # Make sure the user has both city and phone number
            if not user.phone_number or not user.city:
                continue

            location = f"{user.city}, {user.country or ''}".strip()

            weather = self.get_weather_data(location)
            if not weather:
                continue

            condition = weather.get("current", {}).get("condition", "").lower()

            if self.is_bad_weather(condition):
                body = f"⚠️ Alert: Bad weather today in {user.city} — {condition.capitalize()}. Protect your plants!"
            else:
                body = "🌱 Daily reminder: Don't forget to water your plants today!"

            send_sms_notification(user.phone_number, body)

    def get_weather_data(self, location):
        url = "https://yahoo-weather5.p.rapidapi.com/weather"
        headers = {
            "x-rapidapi-key": "e4dae51515msh6f838bf6e9f69c1p1b221ejsn91ee8b271ba6",
            "x-rapidapi-host": "yahoo-weather5.p.rapidapi.com"
        }
        params = {
            "location": location,
            "format": "json",
            "u": "c"
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return {
                "current": {
                    "condition": data.get("current_observation", {}).get("condition", {}).get("text", "")
                }
            }
        except Exception as e:
            print(f"Error getting weather for {location}: {e}")
            return None

    def is_bad_weather(self, condition):
        bad_keywords = ['rain', 'storm', 'snow', 'hail', 'thunder']
        return any(bad in condition for bad in bad_keywords)
