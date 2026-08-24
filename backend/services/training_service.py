from pathlib import Path

import pandas as pd


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


# Number of observations into the future used as the target.
# IBTrACS observations are commonly at 6-hour intervals, but
# this should be verified for your actual dataset.
FUTURE_STEP = 1


# =========================================================
# DATA NORMALIZATION
# =========================================================

def normalize_observations(
    observations: list[dict]
) -> pd.DataFrame:

    rows = []

    for observation in observations:

        rows.append({

            "sid":
                observation.get("sid"),

            "season":
                observation.get("season"),

            "name":
                observation.get("name"),

            "iso_time":
                observation.get("iso_time"),

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

    df = pd.DataFrame(rows)

    if "iso_time" in df.columns:

        df["iso_time"] = pd.to_datetime(
            df["iso_time"],
            errors="coerce"
        )

    return df


# =========================================================
# CREATE TRAINING DATA
# =========================================================

def create_training_dataset(
    observations: list[dict],
    output_path: str
):

    df = normalize_observations(
        observations
    )

    if df.empty:

        raise ValueError(
            "No cyclone observations were supplied."
        )


    # -----------------------------------------------------
    # Sort observations chronologically
    # -----------------------------------------------------

    df = df.sort_values(
        [
            "sid",
            "iso_time"
        ]
    )


    # -----------------------------------------------------
    # Create future targets
    #
    # shift(-1) means:
    #
    # current observation
    #        ↓
    # next observation
    #
    # The model learns the movement between them.
    # -----------------------------------------------------

    grouped = df.groupby(
        "sid",
        group_keys=False
    )


    df["future_latitude"] = grouped[
        "latitude"
    ].shift(
        -FUTURE_STEP
    )


    df["future_longitude"] = grouped[
        "longitude"
    ].shift(
        -FUTURE_STEP
    )


    df["future_wind"] = grouped[
        "wind"
    ].shift(
        -FUTURE_STEP
    )


    df["future_pressure"] = grouped[
        "pressure"
    ].shift(
        -FUTURE_STEP
    )


    # -----------------------------------------------------
    # Calculate movement
    # -----------------------------------------------------

    df["delta_latitude"] = (
        df["future_latitude"]
        - df["latitude"]
    )


    df["delta_longitude"] = (
        df["future_longitude"]
        - df["longitude"]
    )


    # -----------------------------------------------------
    # Remove rows without future observations
    # -----------------------------------------------------

    required_columns = (
        FEATURE_COLUMNS
        + TARGET_COLUMNS
    )


    df = df.dropna(
        subset=required_columns
    )


    if df.empty:

        raise ValueError(
            "No usable training rows remain after "
            "creating future targets."
        )


    # -----------------------------------------------------
    # Save training dataset
    # -----------------------------------------------------

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    df.to_csv(
        output_path,
        index=False
    )


    print(
        "Training dataset created:"
    )

    print(
        output_path
    )

    print(
        f"Training rows: {len(df)}"
    )


    return df


# =========================================================
# LOAD OBSERVATIONS FROM CSV
# =========================================================

def create_training_dataset_from_csv(
    input_path: str,
    output_path: str
):

    input_path = Path(
        input_path
    )

    if not input_path.exists():

        raise FileNotFoundError(
            f"Input dataset not found: {input_path}"
        )


    raw_df = pd.read_csv(
        input_path
    )


    observations = []


    for _, row in raw_df.iterrows():

        observations.append({

            "sid":
                row.get("SID", row.get("sid")),

            "season":
                row.get(
                    "SEASON",
                    row.get("season")
                ),

            "name":
                row.get(
                    "NAME",
                    row.get("name")
                ),

            "iso_time":
                row.get(
                    "ISO_TIME",
                    row.get("iso_time")
                ),

            "latitude":
                row.get(
                    "LAT",
                    row.get("latitude")
                ),

            "longitude":
                row.get(
                    "LON",
                    row.get("longitude")
                ),

            "wind":
                row.get(
                    "USA_WIND",
                    row.get("wind")
                ),

            "pressure":
                row.get(
                    "USA_PRES",
                    row.get("pressure")
                ),

            "storm_speed":
                row.get(
                    "STORM_SPEED",
                    row.get("storm_speed")
                ),

            "storm_direction":
                row.get(
                    "STORM_DIR",
                    row.get("storm_direction")
                ),

            "distance_to_land":
                row.get(
                    "DIST2LAND",
                    row.get("distance_to_land")
                ),

        })


    return create_training_dataset(
        observations,
        output_path
    )


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
# COMMAND LINE
# =========================================================

if __name__ == "__main__":

    create_training_dataset_from_csv(

        input_path=(
            "data/ibtracs.csv"
        ),

        output_path=(
            "data/training/"
            "cyclone_training.csv"
        )

    )