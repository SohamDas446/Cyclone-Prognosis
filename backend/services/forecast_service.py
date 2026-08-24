from typing import Any

import numpy as np


FEATURE_COLUMNS = [
    "latitude",
    "longitude",
    "wind",
    "pressure",
    "storm_speed",
    "storm_direction",
    "distance_to_land",
]


class CycloneForecastService:
    """
    Adapter for the trained cyclone forecasting model.

    Until a real trained model is loaded, this service returns
    available=False instead of generating a fake prediction.
    """

    def __init__(self, model: Any = None):
        self.model = model

    def predict(self, observations: list[dict[str, Any]]) -> dict[str, Any]:
        if self.model is None:
            return {
                "available": False,
                "message": (
                    "Forecast model is not configured yet. "
                    "Current observations can be displayed, but no "
                    "prediction is generated."
                ),
            }

        features = self._prepare_features(observations)

        prediction = self.model.predict(features)

        if hasattr(prediction, "tolist"):
            prediction = prediction.tolist()

        return {
            "available": True,
            "prediction": prediction,
        }

    @staticmethod
    def _prepare_features(
        observations: list[dict[str, Any]],
    ) -> np.ndarray:
        rows = []

        for observation in observations:
            rows.append(
                [
                    _to_float(observation.get("latitude")),
                    _to_float(observation.get("longitude")),
                    _to_float(observation.get("wind")),
                    _to_float(observation.get("pressure")),
                    _to_float(observation.get("storm_speed")),
                    _to_float(observation.get("storm_direction")),
                    _to_float(observation.get("distance_to_land")),
                ]
            )

        return np.asarray(rows, dtype=float)


def _to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return np.nan


forecast_service = CycloneForecastService()
