from typing import Any

import requests


class WeatherService:
    """
    Weather service using the Open-Meteo Forecast API.

    The API is queried directly using the user's
    latitude and longitude.
    """

    def __init__(
        self,
        base_url: str = "https://api.open-meteo.com/v1/forecast",
    ):
        self.base_url = base_url


    def get_current_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> dict[str, Any]:

        # -------------------------------------------------
        # Validate coordinates
        # -------------------------------------------------

        if not -90 <= latitude <= 90:
            raise ValueError(
                "Latitude must be between -90 and 90."
            )

        if not -180 <= longitude <= 180:
            raise ValueError(
                "Longitude must be between -180 and 180."
            )


        # -------------------------------------------------
        # Request current weather
        # -------------------------------------------------

        params = {
            "latitude": latitude,
            "longitude": longitude,

            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "precipitation,"
                "rain,"
                "showers,"
                "weather_code,"
                "cloud_cover,"
                "pressure_msl,"
                "wind_speed_10m,"
                "wind_direction_10m,"
                "wind_gusts_10m"
            ),

            "timezone": "auto",

            "temperature_unit": "celsius",

            "wind_speed_unit": "kmh",

            "precipitation_unit": "mm",
        }


        try:

            response = requests.get(
                self.base_url,
                params=params,
                timeout=15,
            )

            response.raise_for_status()

            data = response.json()


        except requests.RequestException as exc:

            return {
                "available": False,
                "provider": "Open-Meteo",
                "error": str(exc),
            }


        # -------------------------------------------------
        # Extract current conditions
        # -------------------------------------------------

        current = data.get(
            "current",
            {}
        )

        current_units = data.get(
            "current_units",
            {}
        )


        return {

            "available":
                True,

            "provider":
                "Open-Meteo",

            "latitude":
                data.get(
                    "latitude",
                    latitude
                ),

            "longitude":
                data.get(
                    "longitude",
                    longitude
                ),

            "timezone":
                data.get(
                    "timezone"
                ),

            "time":
                current.get(
                    "time"
                ),

            "temperature":
                current.get(
                    "temperature_2m"
                ),

            "temperature_unit":
                current_units.get(
                    "temperature_2m",
                    "°C"
                ),

            "relative_humidity":
                current.get(
                    "relative_humidity_2m"
                ),

            "apparent_temperature":
                current.get(
                    "apparent_temperature"
                ),

            "precipitation":
                current.get(
                    "precipitation"
                ),

            "rain":
                current.get(
                    "rain"
                ),

            "showers":
                current.get(
                    "showers"
                ),

            "weather_code":
                current.get(
                    "weather_code"
                ),

            "cloud_cover":
                current.get(
                    "cloud_cover"
                ),

            "pressure_msl":
                current.get(
                    "pressure_msl"
                ),

            "wind_speed":
                current.get(
                    "wind_speed_10m"
                ),

            "wind_direction":
                current.get(
                    "wind_direction_10m"
                ),

            "wind_gusts":
                current.get(
                    "wind_gusts_10m"
                ),

            "raw":
                data,
        }


# =========================================================
# SINGLE SERVICE INSTANCE
# =========================================================

weather_service = WeatherService()