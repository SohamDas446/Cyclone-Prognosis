import pandas as pd


def load_ibtracs(file_path):
    """
    Load and clean the IBTrACS CSV dataset.
    """

    df = pd.read_csv(file_path, low_memory=False)

    # Remove the first row containing measurement units
    df = df.iloc[1:].copy()

    # Convert important columns to numeric
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
    df["ISO_TIME"] = pd.to_datetime(df["ISO_TIME"], errors="coerce")

    print("IBTrACS dataset loaded and cleaned successfully!")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    return df


if __name__ == "__main__":
    file_path = "data/raw/ibtracs.csv"

    df = load_ibtracs(file_path)

    print("\nCleaned data:")
    print(
        df[
            [
                "SID",
                "SEASON",
                "NAME",
                "ISO_TIME",
                "LAT",
                "LON",
                "USA_WIND",
                "USA_PRES",
                "USA_SSHS",
                "DIST2LAND",
                "STORM_SPEED",
                "STORM_DIR",
            ]
        ].head(10).to_string(index=False)
    )
