from rest_framework import serializers

class ForecastSerializer(serializers.Serializer):
    day = serializers.CharField()
    date = serializers.IntegerField()
    high = serializers.IntegerField()
    low = serializers.IntegerField()
    condition = serializers.CharField(source='text')
    code = serializers.IntegerField()

class CurrentWeatherSerializer(serializers.Serializer):
    temperature = serializers.IntegerField()
    condition = serializers.CharField(source='text')
    code = serializers.IntegerField()

class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField()
    country = serializers.CharField()
    latitude = serializers.FloatField(source='lat')
    longitude = serializers.FloatField(source='long')
    timezone = serializers.CharField(source='timezone_id')
    current = CurrentWeatherSerializer(source='current_observation.condition')
    forecasts = ForecastSerializer(many=True)
