from typing import Any, Iterable

from services.location_service import distance_km


def _get_value(observation: Any, *names: str, default=None):
    """Read a value from either a dictionary or an object."""
    if isinstance(observation, dict):
        for name in names:
            if name in observation:
                return observation[name]
        return default

    for name in names:
        if hasattr(observation, name):
            return getattr(observation, name)

    return default


def find_nearby_cyclones(
    observations: Iterable[Any],
    latitude: float,
    longitude: float,
    radius_km: float = 1000.0,
) -> list[dict[str, Any]]:
    """
    Find cyclone observations within radius_km of a location.

    Accepts dictionaries or database-row-like objects so this can be
    connected to the existing PostgreSQL code without changing it.
    """
    nearby = []

    for observation in observations:
        storm_lat = _get_value(
            observation,
            "latitude",
            "lat",
            "LAT",
        )
        storm_lon = _get_value(
            observation,
            "longitude",
            "lon",
            "LON",
        )

        if storm_lat is None or storm_lon is None:
            continue

        try:
            storm_lat = float(storm_lat)
            storm_lon = float(storm_lon)
        except (TypeError, ValueError):
            continue

        distance = distance_km(
            latitude,
            longitude,
            storm_lat,
            storm_lon,
        )

        if distance <= radius_km:
            if isinstance(observation, dict):
                item = dict(observation)
            else:
                item = {
                    "latitude": storm_lat,
                    "longitude": storm_lon,
                }

            item["distance_km"] = round(distance, 2)
            nearby.append(item)

    nearby.sort(key=lambda item: item["distance_km"])
    return nearby
