import os
from typing import Any

import requests


class WeatherService:
    """Adapter for a configured live weather API."""

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or os.getenv("WEATHER_API_URL")

    def get_current_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> dict[str, Any]:
        if not self.base_url:
            raise RuntimeError(
                "WEATHER_API_URL is not configured. "
                "Add it to backend/.env."
            )

        response = requests.get(
            self.base_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
            },
            timeout=15,
        )
        response.raise_for_status()

        data = response.json()
        return data if isinstance(data, dict) else {"data": data}


weather_service = WeatherService()
