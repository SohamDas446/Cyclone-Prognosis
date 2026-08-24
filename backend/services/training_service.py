from pathlib import Path

import pandas as pd

from services.ibtracs_service import load_ibtracs


# =========================================================
# PATHS
# =========================================================

BACKEND_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = (
    BACKEND_DIR
    / "data"
    / "raw"
    / "ibtracs.csv"
)

TRAINING_DATA_PATH = (
    BACKEND_DIR
    / "data"
    / "training"
    / "cyclone_training.csv"
)


# =========================================================
# MODEL COLUMNS
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


# One observation into the future
FUTURE_STEP = 1


# =========================================================
# CREATE TRAINING DATASET
# =========================================================

def create_training_dataset(
    input_path=RAW_DATA_PATH,
    output_path=TRAINING_DATA_PATH,
):

    input_path = Path(input_path)
    output_path = Path(output_path)

    # -----------------------------------------------------
    # Check raw dataset
    # -----------------------------------------------------

    if not input_path.exists():

        raise FileNotFoundError(
            f"IBTrACS dataset not found: {input_path}"
        )


    print("Loading IBTrACS dataset...")

    # Reuse existing project loader
    df = load_ibtracs(
        input_path
    )


    # -----------------------------------------------------
    # Keep required columns
    # -----------------------------------------------------

    required_ibtracs_columns = [
        "SID",
        "SEASON",
        "NAME",
        "ISO_TIME",
        "LAT",
        "LON",
        "USA_WIND",
        "USA_PRES",
        "DIST2LAND",
        "STORM_SPEED",
        "STORM_DIR",
    ]


    missing_columns = [

        column

        for column in required_ibtracs_columns

        if column not in df.columns

    ]


    if missing_columns:

        raise ValueError(
            "IBTrACS dataset is missing columns: "
            + ", ".join(missing_columns)
        )


    df = df[
        required_ibtracs_columns
    ].copy()


    # -----------------------------------------------------
    # Rename columns to model format
    # -----------------------------------------------------

    df = df.rename(
        columns={
            "SID": "sid",
            "SEASON": "season",
            "NAME": "name",
            "ISO_TIME": "iso_time",
            "LAT": "latitude",
            "LON": "longitude",
            "USA_WIND": "wind",
            "USA_PRES": "pressure",
            "DIST2LAND": "distance_to_land",
            "STORM_SPEED": "storm_speed",
            "STORM_DIR": "storm_direction",
        }
    )


    # -----------------------------------------------------
    # Remove rows without storm ID/time/location
    # -----------------------------------------------------

    df = df.dropna(
        subset=[
            "sid",
            "iso_time",
            "latitude",
            "longitude",
        ]
    )


    # -----------------------------------------------------
    # Sort every cyclone chronologically
    # -----------------------------------------------------

    df = df.sort_values(
        by=[
            "sid",
            "iso_time",
        ]
    ).reset_index(
        drop=True
    )


    # =====================================================
    # CREATE FUTURE TARGETS
    # =====================================================

    grouped = df.groupby(
        "sid",
        sort=False
    )


    # -----------------------------------------------------
    # Future latitude
    # -----------------------------------------------------

    df["future_latitude"] = (
        grouped["latitude"]
        .shift(-FUTURE_STEP)
    )


    # -----------------------------------------------------
    # Future longitude
    # -----------------------------------------------------

    df["future_longitude"] = (
        grouped["longitude"]
        .shift(-FUTURE_STEP)
    )


    # -----------------------------------------------------
    # Future wind
    # -----------------------------------------------------

    df["future_wind"] = (
        grouped["wind"]
        .shift(-FUTURE_STEP)
    )


    # -----------------------------------------------------
    # Future pressure
    # -----------------------------------------------------

    df["future_pressure"] = (
        grouped["pressure"]
        .shift(-FUTURE_STEP)
    )


    # =====================================================
    # CALCULATE MOVEMENT TARGETS
    # =====================================================

    df["delta_latitude"] = (
        df["future_latitude"]
        - df["latitude"]
    )


    df["delta_longitude"] = (
        df["future_longitude"]
        - df["longitude"]
    )


    # =====================================================
    # PREVENT IRREGULAR TIME TARGETS
    # =====================================================

    df["future_time"] = (
        grouped["iso_time"]
        .shift(-FUTURE_STEP)
    )


    df["forecast_hours"] = (
        (
            df["future_time"]
            - df["iso_time"]
        )
        .dt.total_seconds()
        / 3600
    )


    # Keep standard 6-hour forecast pairs.
    #
    # This is much safer than blindly assuming every next
    # row represents exactly six hours.
    df = df[
        df["forecast_hours"] == 6
    ].copy()


    # =====================================================
    # REMOVE INCOMPLETE TRAINING ROWS
    # =====================================================

    required_training_columns = (
        FEATURE_COLUMNS
        + TARGET_COLUMNS
    )


    before_drop = len(df)


    df = df.dropna(
        subset=required_training_columns
    )


    removed = (
        before_drop
        - len(df)
    )


    print(
        f"Removed {removed} incomplete training rows."
    )


    if df.empty:

        raise ValueError(
            "No usable training data remains."
        )


    # =====================================================
    # FINAL TRAINING DATASET
    # =====================================================

    final_columns = [

        "sid",
        "season",
        "name",
        "iso_time",

        *FEATURE_COLUMNS,

        *TARGET_COLUMNS,

        "forecast_hours",

    ]


    training_df = df[
        final_columns
    ].copy()


    # =====================================================
    # SAVE DATASET
    # =====================================================

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    training_df.to_csv(
        output_path,
        index=False
    )


    print()
    print("=" * 60)
    print("TRAINING DATASET CREATED")
    print("=" * 60)

    print(
        f"Output: {output_path}"
    )

    print(
        f"Training rows: {len(training_df)}"
    )

    print(
        f"Unique cyclones: "
        f"{training_df['sid'].nunique()}"
    )

    print(
        f"Seasons: "
        f"{training_df['season'].min()} "
        f"- "
        f"{training_df['season'].max()}"
    )

    print("=" * 60)


    return training_df


# =========================================================
# RUN DIRECTLY
# =========================================================

if __name__ == "__main__":

    create_training_dataset()