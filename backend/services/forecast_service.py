from pathlib import Path
from typing import Any

import joblib
import numpy as np


# =========================================================
# MODEL LOCATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "cyclone_model.joblib"
)


# =========================================================
# FEATURE ORDER
# =========================================================

FEATURE_COLUMNS = [
    "latitude",
    "longitude",
    "wind",
    "pressure",
    "storm_speed",
    "storm_direction",
    "distance_to_land",
]


# =========================================================
# FORECAST SERVICE
# =========================================================

class CycloneForecastService:

    def __init__(
        self,
        model_path: Path = MODEL_PATH
    ):

        self.model_path = Path(
            model_path
        )

        self.model = None

        self.load_model()


    # =====================================================
    # LOAD MODEL
    # =====================================================

    def load_model(self):

        if not self.model_path.exists():

            print(
                "⚠ Forecast model not found:"
            )

            print(
                self.model_path
            )

            print(
                "⚠ Forecasting is currently disabled."
            )

            self.model = None

            return


        try:

            self.model = joblib.load(
                self.model_path
            )

            print(
                "✓ Cyclone forecasting model loaded:"
            )

            print(
                self.model_path
            )

        except Exception as exc:

            print(
                "⚠ Failed to load cyclone model:"
            )

            print(
                exc
            )

            self.model = None


    # =====================================================
    # RELOAD MODEL
    # =====================================================

    def reload_model(self):

        self.load_model()


    # =====================================================
    # PREPARE FEATURES
    # =====================================================

    @staticmethod
    def prepare_features(
        observations: list[dict[str, Any]]
    ):

        rows = []

        for observation in observations:

            rows.append([

                _to_float(
                    observation.get(
                        "latitude"
                    )
                ),

                _to_float(
                    observation.get(
                        "longitude"
                    )
                ),

                _to_float(
                    observation.get(
                        "wind"
                    )
                ),

                _to_float(
                    observation.get(
                        "pressure"
                    )
                ),

                _to_float(
                    observation.get(
                        "storm_speed"
                    )
                ),

                _to_float(
                    observation.get(
                        "storm_direction"
                    )
                ),

                _to_float(
                    observation.get(
                        "distance_to_land"
                    )
                ),

            ])


        return np.asarray(
            rows,
            dtype=float
        )


    # =====================================================
    # PREDICT
    # =====================================================

    def predict(
        self,
        observations: list[dict[str, Any]]
    ):

        # -------------------------------------------------
        # No model
        # -------------------------------------------------

        if self.model is None:

            return {

                "available": False,

                "message": (
                    "Forecast model is not available. "
                    "Train the model and place "
                    "cyclone_model.joblib inside "
                    "backend/models/."
                )

            }


        # -------------------------------------------------
        # No observations
        # -------------------------------------------------

        if not observations:

            return {

                "available": False,

                "message": (
                    "No nearby cyclone observations "
                    "are available for forecasting."
                )

            }


        # -------------------------------------------------
        # Prepare input
        # -------------------------------------------------

        features = self.prepare_features(
            observations
        )


        # -------------------------------------------------
        # Generate prediction
        # -------------------------------------------------

        try:

            predictions = self.model.predict(
                features
            )

        except Exception as exc:

            return {

                "available": False,

                "message": (
                    "Forecast model failed during "
                    "prediction."
                ),

                "error": str(exc)

            }


        # -------------------------------------------------
        # Format results
        # -------------------------------------------------

        results = []


        for observation, prediction in zip(
            observations,
            predictions
        ):

            current_latitude = _to_float(
                observation.get(
                    "latitude"
                )
            )

            current_longitude = _to_float(
                observation.get(
                    "longitude"
                )
            )


            delta_latitude = float(
                prediction[0]
            )

            delta_longitude = float(
                prediction[1]
            )

            predicted_wind = float(
                prediction[2]
            )

            predicted_pressure = float(
                prediction[3]
            )


            predicted_latitude = (
                current_latitude
                + delta_latitude
            )


            predicted_longitude = (
                current_longitude
                + delta_longitude
            )


            results.append({

                "cyclone":
                    observation.get(
                        "name"
                    ),

                "current_latitude":
                    current_latitude,

                "current_longitude":
                    current_longitude,

                "predicted_delta_latitude":
                    delta_latitude,

                "predicted_delta_longitude":
                    delta_longitude,

                "predicted_latitude":
                    predicted_latitude,

                "predicted_longitude":
                    predicted_longitude,

                "predicted_wind":
                    predicted_wind,

                "predicted_pressure":
                    predicted_pressure,

                "distance_km":
                    observation.get(
                        "distance_km"
                    ),

            })


        return {

            "available": True,

            "model":
                str(self.model_path),

            "predictions":
                results

        }


# =========================================================
# UTILITY
# =========================================================

def _to_float(value):

    try:

        return float(value)

    except (
        TypeError,
        ValueError
    ):

        return float("nan")


# =========================================================
# GLOBAL SERVICE INSTANCE
# =========================================================

forecast_service = CycloneForecastService()