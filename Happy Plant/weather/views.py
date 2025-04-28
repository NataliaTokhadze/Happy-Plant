from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import render
import requests

from .serializers import WeatherSerializer, ForecastSerializer, CurrentWeatherSerializer
from notifications.firebase_service import send_push_to_multiple_devices
from notifications.models import DeviceToken  # to get tokens from database

class WeatherViewSet(GenericViewSet):
    def list(self, request):
        return render(request, 'weather/weather_form.html')

    @action(detail=False, methods=['get'])
    def api(self, request):
        city = request.query_params.get('city')
        country = request.query_params.get('country')
        
        if not city:
            return Response({"error": "City parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        weather_data = self.get_weather_data(city, country)
        
        if 'error' in weather_data:
            return Response(weather_data, status=status.HTTP_400_BAD_REQUEST)

        # check weather conditions
        bad_weather = self.is_bad_weather(weather_data)

        # get all device tokens
        tokens = DeviceToken.objects.values_list('token', flat=True)

        if tokens:
            if bad_weather:
                # Send bad weather alert
                send_push_to_multiple_devices(
                    tokens=list(tokens),
                    title="🌧️ Bad Weather Alert!",
                    body=f"Today in {weather_data['city']}: {weather_data['current']['condition']}. Please be careful!"
                )
            else:
                # Send daily reminder
                send_push_to_multiple_devices(
                    tokens=list(tokens),
                    title="🌱 Daily Plant Care",
                    body="Don't forget to water your plants today!"
                )
        
        return Response(weather_data)

    def get_weather_data(self, city, country=None):
        url = "https://yahoo-weather5.p.rapidapi.com/weather"
        
        if country:
            location = f"{city}, {country}"
        else:
            location = city
        
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
            
            weather_info = {
                "city": data.get("location", {}).get("city", "Unknown"),
                "country": data.get("location", {}).get("country", "Unknown"),
                "latitude": data.get("location", {}).get("lat"),
                "longitude": data.get("location", {}).get("long"),
                "timezone": data.get("location", {}).get("timezone_id"),
                "current": {
                    "temperature": data.get("current_observation", {}).get("condition", {}).get("temperature"),
                    "condition": data.get("current_observation", {}).get("condition", {}).get("text"),
                    "code": data.get("current_observation", {}).get("condition", {}).get("code"),
                },
                "forecasts": []
            }
            
            forecasts = data.get("forecasts", [])
            for forecast in forecasts:
                weather_info["forecasts"].append({
                    "day": forecast.get("day"),
                    "date": forecast.get("date"),
                    "high": forecast.get("high"),
                    "low": forecast.get("low"),
                    "condition": forecast.get("text"),
                    "code": forecast.get("code")
                })
            
            return weather_info
        
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except (KeyError, ValueError) as e:
            return {"error": f"Error processing data: {str(e)}"}

    def is_bad_weather(self, weather_data):
        """
        Simple method to decide if weather is bad enough to send a notification.
        """
        condition = weather_data.get('current', {}).get('condition', '').lower()
        bad_conditions = ['rain', 'storm', 'snow', 'hail', 'thunder']

        for bad in bad_conditions:
            if bad in condition:
                return True
        return False
