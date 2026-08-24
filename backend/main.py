from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.database import get_connection
from services.llm_service import ask_llm
from services.rag_service import search_knowledge


app = FastAPI(title="Cyclone AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    cyclone_name: str
    question: str


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

            if season is not None:
                query += " AND season = %s"
                params.append(season)

            if name is not None:
                query += " AND UPPER(name) = UPPER(%s)"
                params.append(name)

            if basin is not None:
                query += " AND UPPER(basin) = UPPER(%s)"
                params.append(basin)

            query += """
                ORDER BY iso_time DESC
                LIMIT %s
            """

            params.append(limit)

            cursor.execute(query, params)

            rows = cursor.fetchall()
            columns = [desc.name for desc in cursor.description]

            return [
                dict(zip(columns, row))
                for row in rows
            ]

    finally:
        conn.close()


@app.get("/cyclones/{name}/summary")
def cyclone_summary(name: str):

    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute("""
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
            """, (name,))

            rows = cursor.fetchall()

            if not rows:
                return {
                    "message": f"Cyclone '{name}' not found"
                }

            columns = [desc.name for desc in cursor.description]

            return [
                dict(zip(columns, row))
                for row in rows
            ]

    finally:
        conn.close()


@app.get("/cyclones/{name}/track")
def cyclone_track(name: str):

    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute("""
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
            """, (name,))

            rows = cursor.fetchall()

            if not rows:
                return {
                    "message": f"Cyclone '{name}' not found"
                }

            columns = [desc.name for desc in cursor.description]

            return [
                dict(zip(columns, row))
                for row in rows
            ]

    finally:
        conn.close()


@app.post("/ask")
def ask_about_cyclone(request: AskRequest):

    # -------------------------------------------------
    # 1. Get cyclone data from PostgreSQL
    # -------------------------------------------------

    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute("""
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
            """, (request.cyclone_name,))

            rows = cursor.fetchall()

            columns = [desc.name for desc in cursor.description]

            cyclone_data = [
                dict(zip(columns, row))
                for row in rows
            ]

    finally:
        conn.close()


    # -------------------------------------------------
    # 2. Retrieve relevant knowledge using RAG
    # -------------------------------------------------

    rag_results = search_knowledge(
        request.question,
        top_k=3
    )


    # -------------------------------------------------
    # 3. Build RAG context
    # -------------------------------------------------

    rag_context = "\n\n".join(
        result["text"]
        for result in rag_results
    )


    # -------------------------------------------------
    # 4. Combine cyclone data + RAG knowledge
    # -------------------------------------------------

    context = f"""
CYCLONE DATA:
{cyclone_data}

RETRIEVED CYCLONE KNOWLEDGE:
{rag_context}
"""


    # -------------------------------------------------
    # 5. Ask the LLM
    # -------------------------------------------------

    answer = ask_llm(
        request.question,
        context
    )


    # -------------------------------------------------
    # 6. Return response
    # -------------------------------------------------

    return {
        "question": request.question,
        "cyclone": request.cyclone_name,
        "answer": answer,
        "cyclone_data": cyclone_data,
        "rag_context": rag_results
    }