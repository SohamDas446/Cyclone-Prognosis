import os
from typing import Any

import requests


class SatelliteService:
    """
    Adapter for a configured satellite-data provider.

    The provider-specific endpoint and authentication are intentionally
    kept outside this module. Configure SATELLITE_API_URL in .env.
    """

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or os.getenv("SATELLITE_API_URL")

    def get_latest_image_metadata(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 500.0,
    ) -> dict[str, Any]:
        if not self.base_url:
            return {
                "available": False,
                "message": (
                    "Satellite API is not configured yet. "
                    "Set SATELLITE_API_URL in backend/.env."
                ),
            }

        response = requests.get(
            self.base_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "radius_km": radius_km,
            },
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()
        return data if isinstance(data, dict) else {"data": data}


satellite_service = SatelliteService()
