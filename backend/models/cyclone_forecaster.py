"""
Cyclone Forecasting Model

This module handles:
1. Preparing cyclone training data
2. Training a baseline forecasting model
3. Saving/loading the trained model

The model predicts:
    - future latitude change
    - future longitude change
    - future wind
    - future pressure

IMPORTANT:
This is a baseline research model. It is NOT an official
meteorological forecasting system.
"""

from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor


# =========================================================
# CONFIGURATION
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

TARGET_COLUMNS = [
    "delta_latitude",
    "delta_longitude",
    "future_wind",
    "future_pressure",
]


MODEL_PATH = Path(
    __file__
).resolve().parent / "cyclone_model.joblib"


# =========================================================
# FORECASTER CLASS
# =========================================================

class CycloneForecaster:

    def __init__(self, model=None):

        self.model = model


    # =====================================================
    # PREPARE FEATURES
    # =====================================================

    @staticmethod
    def prepare_features(
        observations: list[dict]
    ) -> pd.DataFrame:

        rows = []

        for observation in observations:

            rows.append({

                "latitude":
                    _to_float(
                        observation.get("latitude")
                    ),

                "longitude":
                    _to_float(
                        observation.get("longitude")
                    ),

                "wind":
                    _to_float(
                        observation.get("wind")
                    ),

                "pressure":
                    _to_float(
                        observation.get("pressure")
                    ),

                "storm_speed":
                    _to_float(
                        observation.get("storm_speed")
                    ),

                "storm_direction":
                    _to_float(
                        observation.get("storm_direction")
                    ),

                "distance_to_land":
                    _to_float(
                        observation.get("distance_to_land")
                    ),

            })

        return pd.DataFrame(
            rows,
            columns=FEATURE_COLUMNS
        )


    # =====================================================
    # LOAD MODEL
    # =====================================================

    @classmethod
    def load(cls, model_path=MODEL_PATH):

        model_path = Path(model_path)

        if not model_path.exists():

            print(
                f"Forecast model not found: {model_path}"
            )

            return cls(model=None)

        model = joblib.load(model_path)

        print(
            f"Forecast model loaded from: {model_path}"
        )

        return cls(model=model)


    # =====================================================
    # SAVE MODEL
    # =====================================================

    def save(self, model_path=MODEL_PATH):

        if self.model is None:

            raise RuntimeError(
                "Cannot save because no model is loaded."
            )

        model_path = Path(model_path)

        model_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        joblib.dump(
            self.model,
            model_path
        )

        print(
            f"Forecast model saved to: {model_path}"
        )


    # =====================================================
    # PREDICT
    # =====================================================

    def predict(
        self,
        observations: list[dict]
    ):

        if self.model is None:

            return {
                "available": False,

                "message": (
                    "Forecast model is not trained yet."
                )
            }


        if not observations:

            return {
                "available": False,

                "message": (
                    "No cyclone observations available."
                )
            }


        features = self.prepare_features(
            observations
        )


        predictions = self.model.predict(
            features
        )


        results = []


        for observation, prediction in zip(
            observations,
            predictions
        ):

            results.append({

                "cyclone":
                    observation.get("name"),

                "current_latitude":
                    observation.get("latitude"),

                "current_longitude":
                    observation.get("longitude"),

                "predicted_delta_latitude":
                    float(prediction[0]),

                "predicted_delta_longitude":
                    float(prediction[1]),

                "predicted_latitude":
                    float(
                        observation.get("latitude")
                    )
                    + float(prediction[0]),

                "predicted_longitude":
                    float(
                        observation.get("longitude")
                    )
                    + float(prediction[1]),

                "predicted_wind":
                    float(prediction[2]),

                "predicted_pressure":
                    float(prediction[3]),

                "distance_km":
                    observation.get("distance_km"),

            })


        return {

            "available": True,

            "predictions": results

        }


# =========================================================
# TRAINING FUNCTION
# =========================================================

def train_model(
    training_csv: str,
    output_path=MODEL_PATH
):

    training_csv = Path(
        training_csv
    )


    if not training_csv.exists():

        raise FileNotFoundError(
            f"Training dataset not found: "
            f"{training_csv}"
        )


    df = pd.read_csv(
        training_csv
    )


    required_columns = (
        FEATURE_COLUMNS
        + TARGET_COLUMNS
    )


    missing_columns = [

        column

        for column in required_columns

        if column not in df.columns

    ]


    if missing_columns:

        raise ValueError(

            "Training dataset is missing "
            "the following columns: "

            + ", ".join(missing_columns)

        )


    # -----------------------------------------------------
    # Remove incomplete rows
    # -----------------------------------------------------

    df = df.dropna(
        subset=required_columns
    )


    if df.empty:

        raise ValueError(
            "No usable training rows remain."
        )


    X = df[
        FEATURE_COLUMNS
    ]


    y = df[
        TARGET_COLUMNS
    ]


    # -----------------------------------------------------
    # Random Forest baseline
    # -----------------------------------------------------

    base_model = RandomForestRegressor(

        n_estimators=300,

        max_depth=None,

        random_state=42,

        n_jobs=-1

    )


    model = MultiOutputRegressor(
        base_model
    )


    print(
        "Training cyclone forecasting model..."
    )


    model.fit(
        X,
        y
    )


    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    output_path = Path(
        output_path
    )


    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    joblib.dump(
        model,
        output_path
    )


    print(
        "Model saved to:"
    )

    print(
        output_path
    )


    return model


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
# COMMAND-LINE TRAINING
# =========================================================

if __name__ == "__main__":

    train_model(

        training_csv=(
            "data/training/"
            "cyclone_training.csv"
        ),

        output_path=MODEL_PATH

    )