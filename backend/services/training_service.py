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


# =========================================================
# FORECAST WINDOW
# =========================================================

TARGET_HOURS = 6

# Accept small timestamp differences around the target.
MIN_FORECAST_HOURS = 5
MAX_FORECAST_HOURS = 7


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
    # Check dataset
    # -----------------------------------------------------

    if not input_path.exists():

        raise FileNotFoundError(
            f"IBTrACS dataset not found: {input_path}"
        )

    print("Loading IBTrACS dataset...")

    df = load_ibtracs(input_path)

    # -----------------------------------------------------
    # Required columns
    # -----------------------------------------------------

    required_columns = [
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
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "IBTrACS dataset is missing columns: "
            + ", ".join(missing_columns)
        )

    # -----------------------------------------------------
    # Select and rename columns
    # -----------------------------------------------------

    df = df[required_columns].copy()

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
    # Make sure timestamp is datetime
    # -----------------------------------------------------

    df["iso_time"] = pd.to_datetime(
        df["iso_time"],
        errors="coerce"
    )

    # -----------------------------------------------------
    # Sort chronologically
    # -----------------------------------------------------

    df = df.dropna(
        subset=[
            "sid",
            "iso_time",
            "latitude",
            "longitude",
        ]
    )

    df = df.sort_values(
        [
            "sid",
            "iso_time",
        ]
    ).reset_index(drop=True)

    print(
        f"Usable observations before pairing: {len(df)}"
    )

    # =====================================================
    # CREATE FUTURE OBSERVATIONS
    # =====================================================

    grouped = df.groupby(
        "sid",
        sort=False
    )

    df["future_latitude"] = (
        grouped["latitude"]
        .shift(-1)
    )

    df["future_longitude"] = (
        grouped["longitude"]
        .shift(-1)
    )

    df["future_wind"] = (
        grouped["wind"]
        .shift(-1)
    )

    df["future_pressure"] = (
        grouped["pressure"]
        .shift(-1)
    )

    df["future_time"] = (
        grouped["iso_time"]
        .shift(-1)
    )

    # =====================================================
    # CALCULATE TIME DIFFERENCE
    # =====================================================

    df["forecast_hours"] = (
        (
            df["future_time"]
            - df["iso_time"]
        )
        .dt.total_seconds()
        / 3600
    )

    # -----------------------------------------------------
    # Show actual interval information
    # -----------------------------------------------------

    valid_intervals = df[
        "forecast_hours"
    ].dropna()

    print()
    print(
        "Forecast interval statistics:"
    )

    print(
        valid_intervals.describe()
    )

    # =====================================================
    # KEEP APPROXIMATELY 6-HOUR PAIRS
    # =====================================================

    df = df[
        (
            df["forecast_hours"]
            >= MIN_FORECAST_HOURS
        )
        &
        (
            df["forecast_hours"]
            <= MAX_FORECAST_HOURS
        )
    ].copy()

    print()
    print(
        "Rows after 6-hour pairing:",
        len(df)
    )

    # =====================================================
    # CREATE TARGETS
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
    # REMOVE INCOMPLETE ROWS
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
        f"Removed {removed} incomplete "
        "training rows."
    )

    if df.empty:

        raise ValueError(
            "No usable training data remains "
            "after creating 6-hour pairs."
        )

    # =====================================================
    # FINAL DATASET
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
    # SAVE
    # =====================================================

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    training_df.to_csv(
        output_path,
        index=False
    )

    # =====================================================
    # SUMMARY
    # =====================================================

    print()
    print("=" * 60)
    print("TRAINING DATASET CREATED SUCCESSFULLY")
    print("=" * 60)

    print(
        f"Output file:\n{output_path}"
    )

    print(
        f"\nTraining rows: "
        f"{len(training_df)}"
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

    print(
        f"Average forecast interval: "
        f"{training_df['forecast_hours'].mean():.2f} hours"
    )

    print("=" * 60)

    return training_df


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    create_training_dataset()