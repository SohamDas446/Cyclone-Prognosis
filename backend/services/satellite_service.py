from datetime import datetime, timezone


class SatelliteService:

    def __init__(self):
        """
        NASA GIBS satellite imagery service.

        GIBS provides map-ready Earth imagery through
        standard WMS/WMTS services.
        """

        self.wms_url = (
            "https://gibs.earthdata.nasa.gov/"
            "wmts/epsg3857/best/"
        )

        self.layer = "MODIS_Terra_CorrectedReflectance_TrueColor"


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
        # NASA GIBS WMTS tile endpoint
        # -------------------------------------------------

        tile_url = (
            "https://gibs.earthdata.nasa.gov/"
            "wmts/epsg3857/best/"
            f"{self.layer}/default/"
            "2026-08-24/"
            "GoogleMapsCompatible_Level9/"
            "{z}/{y}/{x}.jpg"
        )


        # -------------------------------------------------
        # Return metadata
        # -------------------------------------------------

        return {

            "available":
                True,

            "provider":
                "NASA GIBS",

            "layer":
                self.layer,

            "latitude":
                latitude,

            "longitude":
                longitude,

            "radius_km":
                radius_km,

            "tile_url":
                tile_url,

            "updated_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "description":
                (
                    "NASA MODIS Terra corrected-reflectance "
                    "true-color satellite imagery."
                )

        }


# =========================================================
# SINGLE SERVICE INSTANCE
# =========================================================

satellite_service = SatelliteService()