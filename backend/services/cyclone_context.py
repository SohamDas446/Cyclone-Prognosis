from services.database import get_connection


def get_cyclone_context(name: str):
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
                return None

            columns = [desc.name for desc in cursor.description]

            results = [
                dict(zip(columns, row))
                for row in rows
            ]

            return results

    finally:
        conn.close()