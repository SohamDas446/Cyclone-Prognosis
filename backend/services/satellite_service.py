from datetime import datetime, timezone


class SatelliteService:

    def __init__(self):

        self.provider = "NASA GIBS"

        self.layer = (
            "MODIS_Terra_CorrectedReflectance_TrueColor"
        )

        self.base_url = (
            "https://gibs.earthdata.nasa.gov/"
            "wmts/epsg3857/best"
        )


    def get_latest_image_metadata(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 500
    ):

        # -------------------------------------------------
        # Validate coordinates
        # -------------------------------------------------

        if not -90 <= latitude <= 90:

            raise ValueError(
                "Latitude must be between -90 and 90."
            )


        if not -180 <= longitude <= 180:

            raise ValueError(
                "Longitude must be between -180 and 180."
            )


        # -------------------------------------------------
        # Use the current UTC date as the requested
        # imagery date.
        #
        # The frontend will use the map URL rather than
        # treating this as a guaranteed real-time image.
        # -------------------------------------------------

        date_string = (
            datetime.now(
                timezone.utc
            )
            .strftime("%Y-%m-%d")
        )


        # -------------------------------------------------
        # Metadata
        # -------------------------------------------------

        return {

            "available":
                True,

            "provider":
                self.provider,

            "layer":
                self.layer,

            "latitude":
                latitude,

            "longitude":
                longitude,

            "radius_km":
                radius_km,

            "date":
                date_string,

            "imagery_type":
                "MODIS Terra true-color",

            "map_service":
                self.base_url,

            "description":
                (
                    "NASA GIBS satellite imagery layer. "
                    "Availability and acquisition time "
                    "depend on the selected satellite "
                    "product."
                )

        }


# =========================================================
# SINGLE SERVICE INSTANCE
# =========================================================

satellite_service = SatelliteService()