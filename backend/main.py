from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from services.database import get_connection
from services.llm_service import ask_llm
from services.rag_service import search_knowledge

from services.location_service import validate_location
from services.weather_service import weather_service
from services.satellite_service import satellite_service
from services.cyclone_service import find_nearby_cyclones
from services.forecast_service import forecast_service
from services.risk_service import calculate_risk


# =========================================================
# APP CONFIGURATION
# =========================================================

app = FastAPI(
    title="Cyclone AI",
    description="Cyclone analytics, live location analysis and AI assistance.",
    version="2.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# REQUEST MODELS
# =========================================================

class AskRequest(BaseModel):
    cyclone_name: str
    question: str


class LocationRequest(BaseModel):
    latitude: float = Field(
        ...,
        ge=-90,
        le=90
    )

    longitude: float = Field(
        ...,
        ge=-180,
        le=180
    )


class LiveAnalysisRequest(LocationRequest):

    radius_km: float = Field(
        default=1000.0,
        gt=0,
        le=5000
    )

    question: str | None = None


# =========================================================
# BASIC ENDPOINTS
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Cyclone AI Backend is running!"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =========================================================
# GET CYCLONES
# =========================================================

@app.get("/cyclones")
def get_cyclones(
    season: int | None = None,
    name: str | None = None,
    basin: str | None = None,
    limit: int = 10
):

    conn = get_connection()

    try:

        with conn.cursor() as cursor:

            query = """
                SELECT
                    id,
                    sid,
                    season,
                    name,
                    basin,
                    iso_time,
                    nature,
                    lat,
                    lon,
                    usa_wind,
                    usa_pres,
                    usa_sshs,
                    dist2land,
                    storm_speed,
                    storm_dir
                FROM cyclone_observations
                WHERE 1=1
            """

            params = []

            # Season filter
            if season is not None:

                query += """
                    AND season = %s
                """

                params.append(season)

            # Name filter
            if name is not None:

                query += """
                    AND UPPER(name) = UPPER(%s)
                """

                params.append(name)

            # Basin filter
            if basin is not None:

                query += """
                    AND UPPER(basin) = UPPER(%s)
                """

                params.append(basin)

            query += """
                ORDER BY iso_time DESC
                LIMIT %s
            """

            params.append(limit)

            cursor.execute(
                query,
                params
            )

            rows = cursor.fetchall()

            columns = [
                desc.name
                for desc in cursor.description
            ]

            return [
                dict(zip(columns, row))
                for row in rows
            ]

    finally:

        conn.close()


# =========================================================
# CYCLONE SUMMARY
# =========================================================

@app.get("/cyclones/{name}/summary")
def cyclone_summary(name: str):

    conn = get_connection()

    try:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    name,
                    season,
                    COUNT(*) AS observation_count,
                    MAX(usa_wind) AS max_wind,
                    MIN(usa_pres) AS min_pressure,
                    MAX(usa_sshs) AS max_sshs,
                    MIN(iso_time) AS start_time,
                    MAX(iso_time) AS end_time
                FROM cyclone_observations
                WHERE UPPER(name) = UPPER(%s)
                GROUP BY name, season
                ORDER BY season DESC
                """,
                (name,)
            )

            rows = cursor.fetchall()

            if not rows:

                return {
                    "message": f"Cyclone '{name}' not found"
                }

            columns = [
                desc.name
                for desc in cursor.description
            ]

            return [
                dict(zip(columns, row))
                for row in rows
            ]

    finally:

        conn.close()


# =========================================================
# CYCLONE TRACK
# =========================================================

@app.get("/cyclones/{name}/track")
def cyclone_track(name: str):

    conn = get_connection()

    try:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    iso_time,
                    lat,
                    lon,
                    usa_wind,
                    usa_pres,
                    usa_sshs
                FROM cyclone_observations
                WHERE UPPER(name) = UPPER(%s)
                ORDER BY iso_time ASC
                """,
                (name,)
            )

            rows = cursor.fetchall()

            if not rows:

                return {
                    "message": f"Cyclone '{name}' not found"
                }

            columns = [
                desc.name
                for desc in cursor.description
            ]

            return [
                dict(zip(columns, row))
                for row in rows
            ]

    finally:

        conn.close()


# =========================================================
# RAG + LLM CYCLONE CHAT
# =========================================================

@app.post("/ask")
def ask_about_cyclone(request: AskRequest):

    # -----------------------------------------------------
    # 1. Get cyclone information from PostgreSQL
    # -----------------------------------------------------

    conn = get_connection()

    try:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    name,
                    season,
                    COUNT(*) AS observation_count,
                    MAX(usa_wind) AS max_wind,
                    MIN(usa_pres) AS min_pressure,
                    MAX(usa_sshs) AS max_sshs,
                    MIN(iso_time) AS start_time,
                    MAX(iso_time) AS end_time
                FROM cyclone_observations
                WHERE UPPER(name) = UPPER(%s)
                GROUP BY name, season
                ORDER BY season DESC
                """,
                (request.cyclone_name,)
            )

            rows = cursor.fetchall()

            columns = [
                desc.name
                for desc in cursor.description
            ]

            cyclone_data = [
                dict(zip(columns, row))
                for row in rows
            ]

    finally:

        conn.close()

    # -----------------------------------------------------
    # 2. Search knowledge base using RAG
    # -----------------------------------------------------

    rag_results = search_knowledge(
        request.question,
        top_k=3
    )

    # -----------------------------------------------------
    # 3. Build RAG context
    # -----------------------------------------------------

    rag_context = "\n\n".join(
        result["text"]
        for result in rag_results
    )

    # -----------------------------------------------------
    # 4. Combine cyclone data + RAG knowledge
    # -----------------------------------------------------

    context = f"""
CYCLONE DATA:

{cyclone_data}


RETRIEVED CYCLONE KNOWLEDGE:

{rag_context}
"""

    # -----------------------------------------------------
    # 5. Ask LLM
    # -----------------------------------------------------

    answer = ask_llm(
        request.question,
        context
    )

    # -----------------------------------------------------
    # 6. Return response
    # -----------------------------------------------------

    return {

        "question": request.question,

        "cyclone": request.cyclone_name,

        "answer": answer,

        "cyclone_data": cyclone_data,

        "rag_context": rag_results

    }


# =========================================================
# LOCATION ENDPOINT
# =========================================================

@app.post("/location")
def set_location(request: LocationRequest):

    try:

        location = validate_location(
            request.latitude,
            request.longitude
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    return {

        "success": True,

        "location": location

    }


# =========================================================
# LIVE ANALYSIS
# =========================================================

@app.post("/live-analysis")
def live_analysis(
    request: LiveAnalysisRequest
):

    # =====================================================
    # 1. VALIDATE LOCATION
    # =====================================================

    try:

        location = validate_location(
            request.latitude,
            request.longitude
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc


    # =====================================================
    # 2. GET LIVE WEATHER
    # =====================================================

    try:

        weather = weather_service.get_current_weather(
            request.latitude,
            request.longitude
        )

    except Exception as exc:

        weather = {

            "available": False,

            "error": str(exc)

        }


    # =====================================================
    # 3. GET LATEST CYCLONE OBSERVATIONS
    # =====================================================

    conn = get_connection()

    try:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT DISTINCT ON (UPPER(name), season)

                    id,

                    sid,

                    season,

                    name,

                    basin,

                    iso_time,

                    nature,

                    lat,

                    lon,

                    usa_wind,

                    usa_pres,

                    usa_sshs,

                    dist2land,

                    storm_speed,

                    storm_dir

                FROM cyclone_observations

                WHERE lat IS NOT NULL

                  AND lon IS NOT NULL

                  AND name IS NOT NULL

                ORDER BY

                    UPPER(name),

                    season,

                    iso_time DESC
                """
            )

            rows = cursor.fetchall()

            columns = [
                desc.name
                for desc in cursor.description
            ]

            observations = [

                dict(
                    zip(columns, row)
                )

                for row in rows

            ]

    finally:

        conn.close()


    # =====================================================
    # 4. NORMALIZE DATABASE DATA
    # =====================================================

    normalized_observations = []

    for observation in observations:

        normalized_observations.append({

            "id":
                observation.get("id"),

            "sid":
                observation.get("sid"),

            "season":
                observation.get("season"),

            "name":
                observation.get("name"),

            "basin":
                observation.get("basin"),

            "iso_time":
                observation.get("iso_time"),

            "nature":
                observation.get("nature"),

            "latitude":
                observation.get("lat"),

            "longitude":
                observation.get("lon"),

            "wind":
                observation.get("usa_wind"),

            "pressure":
                observation.get("usa_pres"),

            "sshs":
                observation.get("usa_sshs"),

            "distance_to_land":
                observation.get("dist2land"),

            "storm_speed":
                observation.get("storm_speed"),

            "storm_direction":
                observation.get("storm_dir")

        })


    # =====================================================
    # 5. FIND CYCLONES NEAR USER
    # =====================================================

    nearby_cyclones = find_nearby_cyclones(

        normalized_observations,

        request.latitude,

        request.longitude,

        request.radius_km

    )


    # =====================================================
    # 6. GET SATELLITE INFORMATION
    # =====================================================

    try:

        satellite = (
            satellite_service
            .get_latest_image_metadata(

                request.latitude,

                request.longitude,

                request.radius_km

            )
        )

    except Exception as exc:

        satellite = {

            "available": False,

            "error": str(exc)

        }


    # =====================================================
    # 7. RUN FORECAST SERVICE
    # =====================================================

    forecast = forecast_service.predict(

        nearby_cyclones

    )


    # =====================================================
    # 8. CALCULATE RISK
    # =====================================================

    nearest_distance = None

    if nearby_cyclones:

        nearest_distance = (
            nearby_cyclones[0]
            .get("distance_km")
        )


    risk = calculate_risk(

        distance_km=nearest_distance,

        predicted_wind=None,

        landfall_probability=None

    )


    # =====================================================
    # 9. OPTIONAL RAG + LLM
    # =====================================================

    ai_explanation = None

    rag_results = []


    if request.question:

        # -------------------------------------------------
        # Retrieve knowledge
        # -------------------------------------------------

        rag_results = search_knowledge(

            request.question,

            top_k=3

        )


        # -------------------------------------------------
        # Build RAG context
        # -------------------------------------------------

        rag_context = "\n\n".join(

            result["text"]

            for result in rag_results

        )


        # -------------------------------------------------
        # Combine all live information
        # -------------------------------------------------

        live_context = f"""

USER LOCATION:

{location}


CURRENT WEATHER:

{weather}


NEARBY CYCLONES:

{nearby_cyclones}


SATELLITE INFORMATION:

{satellite}


FORECAST:

{forecast}


RISK:

{risk}


RETRIEVED CYCLONE KNOWLEDGE:

{rag_context}

"""


        # -------------------------------------------------
        # Ask LLM
        # -------------------------------------------------

        ai_explanation = ask_llm(

            request.question,

            live_context

        )


    # =====================================================
    # 10. RETURN COMPLETE ANALYSIS
    # =====================================================

    return {

        "location":
            location,

        "weather":
            weather,

        "nearby_cyclones":
            nearby_cyclones,

        "satellite":
            satellite,

        "forecast":
            forecast,

        "risk":
            risk,

        "ai_explanation":
            ai_explanation,

        "rag_context":
            rag_results,

        "disclaimer":
            (
                "This is a research and decision-support "
                "system. Forecasts are model estimates and "
                "are not official meteorological warnings."
            )

    }