def calculate_risk(
    distance_km: float | None,
    predicted_wind: float | None,
    landfall_probability: float | None,
) -> dict:
    """
    Prototype risk score for application/UI use.

    This is NOT an official cyclone warning classification.
    Official warnings should come from the relevant meteorological
    authority.
    """
    score = 0.0

    if distance_km is not None:
        distance = float(distance_km)

        if distance < 200:
            score += 40
        elif distance < 500:
            score += 25
        elif distance < 1000:
            score += 10

    if predicted_wind is not None:
        wind = float(predicted_wind)

        if wind >= 120:
            score += 30
        elif wind >= 80:
            score += 20
        elif wind >= 50:
            score += 10

    if landfall_probability is not None:
        probability = max(
            0.0,
            min(1.0, float(landfall_probability)),
        )
        score += probability * 30

    if score >= 70:
        level = "EXTREME"
    elif score >= 50:
        level = "HIGH"
    elif score >= 25:
        level = "MODERATE"
    else:
        level = "LOW"

    return {
        "score": round(score, 2),
        "level": level,
        "is_official_warning": False,
    }
