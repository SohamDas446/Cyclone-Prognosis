from math import radians, sin, cos, sqrt, atan2


def validate_location(latitude: float, longitude: float) -> dict:
    """Validate geographic coordinates."""
    if not -90 <= latitude <= 90:
        raise ValueError("Invalid latitude. Must be between -90 and 90.")

    if not -180 <= longitude <= 180:
        raise ValueError("Invalid longitude. Must be between -180 and 180.")

    return {
        "latitude": float(latitude),
        "longitude": float(longitude),
    }


def distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two coordinates in km."""
    earth_radius_km = 6371.0

    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    dlat = lat2_rad - lat1_rad
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return earth_radius_km * c
