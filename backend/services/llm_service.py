def ask_llm(question: str, context: str = ""):
    """
    Temporary local LLM replacement.

    This allows the /ask endpoint to work without
    using OpenAI API credits.
    """

    question_lower = question.lower()

    # Try to extract useful cyclone values from the context
    if "max_wind" in context.lower() or "minimum pressure" in question_lower or "low pressure" in question_lower:

        # Extract values if they exist in the context
        import re

        wind_match = re.search(
            r"'max_wind':\s*([0-9.]+)",
            context
        )

        pressure_match = re.search(
            r"'min_pressure':\s*([0-9.]+)",
            context
        )

        sshs_match = re.search(
            r"'max_sshs':\s*([0-9]+)",
            context
        )

        wind = wind_match.group(1) if wind_match else "not available"
        pressure = pressure_match.group(1) if pressure_match else "not available"
        sshs = sshs_match.group(1) if sshs_match else "not available"

        answer = (
            f"The available data shows a maximum wind speed of {wind} "
            f"and a minimum central pressure of {pressure} hPa. "
        )

        if sshs != "not available":
            answer += f"The maximum recorded SSHS category was {sshs}. "

        if pressure != "not available":
            answer += (
                f"The very low central pressure indicates that the cyclone "
                f"was very intense. In general, stronger tropical cyclones "
                f"tend to have lower central pressures."
            )

        return answer

    # Generic fallback
    return (
        "I found relevant cyclone information in the database and "
        "knowledge base, but a natural-language LLM response is "
        "currently unavailable because the OpenAI API has no remaining credits."
    )