from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import render
import requests
from .serializers import WeatherSerializer, ForecastSerializer, CurrentWeatherSerializer

class WeatherViewSet(GenericViewSet):
    """
    ViewSet for weather information.
    """
    
    def list(self, request):
        """
        Render the weather form template.
        GET /weather/
        """
        return render(request, 'weather/weather_form.html')
    
    @action(detail=False, methods=['get'])
    def api(self, request):
        """
        Get weather data for a specified city and country.
        GET /weather/api/?city=<city>&country=<country>
        """
        city = request.query_params.get('city')
        country = request.query_params.get('country')
        
        if not city:
            return Response({"error": "City parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        weather_data = self.get_weather_data(city, country)
        
        if 'error' in weather_data:
            return Response(weather_data, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(weather_data)
    
    def get_weather_data(self, city, country=None):
        """
        Get weather information for a specified city and optionally country
        
        Args:
            city (str): The name of the city
            country (str, optional): The name of the country
        
        Returns:
            dict: Weather information or error message
        """
        url = "https://yahoo-weather5.p.rapidapi.com/weather"
        
        # If both city and country are provided, format the location as "city, country"
        if country:
            location = f"{city}, {country}"
        else:
            location = city
        
        querystring = {
            "location": location,
            "format": "json",
            "u": "c"  # Fahrenheit, change to "c" for Celsius
        }
        
        headers = {
            "x-rapidapi-key": "e4dae51515msh6f838bf6e9f69c1p1b221ejsn91ee8b271ba6",
            "x-rapidapi-host": "yahoo-weather5.p.rapidapi.com"
        }
        
        try:
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            data = response.json()
            
            # Extract relevant information from the response
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
            
            # Extract forecast information
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
