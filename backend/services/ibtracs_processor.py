import pandas as pd


# Columns needed by OceanProject
SELECTED_COLUMNS = [
    "SID",
    "SEASON",
    "NAME",
    "BASIN",
    "ISO_TIME",
    "NATURE",
    "LAT",
    "LON",
    "USA_WIND",
    "USA_PRES",
    "USA_SSHS",
    "DIST2LAND",
    "STORM_SPEED",
    "STORM_DIR",
]


def process_ibtracs(file_path):
    """
    Load the raw IBTrACS dataset and create a clean,
    focused dataframe for OceanProject.
    """

    print("Loading IBTrACS dataset...")

    df = pd.read_csv(file_path, low_memory=False)

    # Remove the first row containing measurement units
    df = df.iloc[1:].copy()

    # Keep only the columns required by OceanProject
    df = df[SELECTED_COLUMNS].copy()

    # Convert numeric columns
    numeric_columns = [
        "SEASON",
        "LAT",
        "LON",
        "USA_WIND",
        "USA_PRES",
        "USA_SSHS",
        "DIST2LAND",
        "STORM_SPEED",
        "STORM_DIR",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Convert timestamp
    df["ISO_TIME"] = pd.to_datetime(
        df["ISO_TIME"],
        errors="coerce"
    )

    # Remove rows without essential location/time information
    df = df.dropna(
        subset=["SID", "ISO_TIME", "LAT", "LON"]
    )

    print("IBTrACS processing completed!")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    return df


if __name__ == "__main__":

    input_file = "data/raw/ibtracs.csv"

    df = process_ibtracs(input_file)

    print("\nProcessed columns:")
    print(df.columns.tolist())

    print("\nFirst 5 processed records:")
    print(df.head().to_string(index=False))
    output_file = "data/processed/ibtracs_clean.csv"

    df.to_csv(output_file, index=False)

    print("\nProcessed dataset saved to:")
    print(output_file)