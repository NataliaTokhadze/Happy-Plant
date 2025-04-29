from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
import requests

from users.models import User
from notifications.twilio_service import send_sms_notification


class WeatherViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]  # Require user to be logged in

    @action(detail=False, methods=['get'])
    def api(self, request):
        user = request.user
        city = user.city
        country = user.country

        if not city:
            return Response({"error": "Your profile is missing a city."}, status=status.HTTP_400_BAD_REQUEST)

        weather_data = self.get_weather_data(city, country)

        if 'error' in weather_data:
            return Response(weather_data, status=status.HTTP_400_BAD_REQUEST)

        # Check if weather is bad
        if self.is_bad_weather(weather_data):
            message = f"⚠️ Weather Alert in {city}: {weather_data['current']['condition']}. Protect your plants!"
        else:
            message = "🌿 Daily Reminder: Don't forget to water your plants today!"

        # Send SMS
        if user.phone_number:
            send_sms_notification(to_number=user.phone_number, body=message)

        return Response(weather_data)

    def get_weather_data(self, city, country=None):
        url = "https://yahoo-weather5.p.rapidapi.com/weather"

        location = f"{city}, {country}" if country else city
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
                "city": data.get("location", {}).get("city", "Unknown"),
                "country": data.get("location", {}).get("country", "Unknown"),
                "current": {
                    "condition": data.get("current_observation", {}).get("condition", {}).get("text", "No info")
                }
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except (KeyError, ValueError) as e:
            return {"error": f"Error processing weather data: {str(e)}"}

    def is_bad_weather(self, weather_data):
        condition = weather_data.get('current', {}).get('condition', '').lower()
        bad_conditions = ['rain', 'storm', 'snow', 'hail', 'thunder']
        return any(bad in condition for bad in bad_conditions)
