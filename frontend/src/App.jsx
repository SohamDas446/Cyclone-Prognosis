import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
    const [location, setLocation] = useState("Kolkata");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const [analysis, setAnalysis] = useState(null);

    // --------------------------------------------------
    // Analyze location
    // --------------------------------------------------

    const analyzeLocation = async () => {
        setLoading(true);
        setError("");

        try {
            // Kolkata coordinates
            // Later we can add a proper location/geocoding system.
            const latitude = 22.5726;
            const longitude = 88.3639;

            const response = await fetch(
                `${API_URL}/live-analysis`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json",
                    },

                    body: JSON.stringify({
                        latitude: latitude,
                        longitude: longitude,
                        radius_km: 1000,
                    }),
                }
            );

            if (!response.ok) {
                throw new Error(
                    `Backend returned ${response.status}`
                );
            }

            const data = await response.json();

            console.log("LIVE ANALYSIS:", data);

            setAnalysis(data);
        }

        catch (err) {
            console.error(err);

            setError(
                "Could not connect to the cyclone analysis server."
            );
        }

        finally {
            setLoading(false);
        }
    };


    // --------------------------------------------------
    // Extract backend data
    // --------------------------------------------------

    const risk = analysis?.risk;

    const weather = analysis?.weather;

    const nearbyCyclones =
        analysis?.nearby_cyclones || [];

    const forecast =
        analysis?.forecast;


    return (
        <div className="app">

            {/* =================================================
                HEADER
            ================================================= */}

            <header className="header">

                <div className="logo">

                    <div className="logo-circle">
                        ◌
                    </div>

                    <div>
                        <div className="logo-title">
                            CYCLONE
                        </div>

                        <div className="logo-subtitle">
                            PROGNOSIS
                        </div>
                    </div>

                </div>


                <nav>

                    <a href="#monitor">
                        Monitor
                    </a>

                    <a href="#forecast">
                        Forecast
                    </a>

                    <a href="#ai">
                        AI Analysis
                    </a>

                </nav>


                <div className="system-status">

                    <span className="status-dot"></span>

                    SYSTEM ONLINE

                </div>

            </header>


            {/* =================================================
                HERO
            ================================================= */}

            <main>

                <section className="hero">

                    <div className="eyebrow">
                        INTELLIGENT CYCLONE MONITORING
                    </div>

                    <h1>
                        Understand the storm.
                        <br />

                        <span>
                            Stay ahead.
                        </span>
                    </h1>

                    <p>
                        Real-time cyclone intelligence powered by
                        weather data, machine learning,
                        satellite imagery and AI.
                    </p>


                    {/* =========================================
                        LOCATION INPUT
                    ========================================= */}

                    <div className="location-box">

                        <div className="location-icon">
                            ⌖
                        </div>

                        <div className="location-input-wrapper">

                            <label>
                                ANALYZE LOCATION
                            </label>

                            <input
                                value={location}
                                onChange={(event) =>
                                    setLocation(
                                        event.target.value
                                    )
                                }
                            />

                        </div>


                        <button
                            onClick={analyzeLocation}
                            disabled={loading}
                        >

                            {loading
                                ? "Analyzing..."
                                : "Analyze"
                            }

                            {!loading && (
                                <span>
                                    →
                                </span>
                            )}

                        </button>

                    </div>


                    {/* =========================================
                        ERROR
                    ========================================= */}

                    {error && (

                        <div className="error-message">
                            {error}
                        </div>

                    )}


                    {/* =========================================
                        DASHBOARD
                    ========================================= */}

                    <section className="dashboard">


                        {/* =====================================
                            CYCLONE ACTIVITY
                        ===================================== */}

                        <div
                            className="card cyclone-card"
                            id="monitor"
                        >

                            <div className="card-header">

                                <div>

                                    <div className="card-label">
                                        LIVE MONITOR
                                    </div>

                                    <h2>
                                        Cyclone Activity
                                    </h2>

                                </div>

                                <div className="live">

                                    <span className="status-dot"></span>

                                    LIVE

                                </div>

                            </div>


                            <div className="cyclone-content">

                                {!analysis && !loading && (

                                    <div className="empty-state">

                                        Click
                                        <strong>
                                            Analyze
                                        </strong>
                                        to retrieve live cyclone
                                        information.

                                    </div>

                                )}


                                {loading && (

                                    <div className="empty-state">

                                        Fetching live cyclone
                                        information...

                                    </div>

                                )}


                                {analysis &&
                                    nearbyCyclones.length === 0 && (

                                        <div className="empty-state">

                                            No nearby cyclones found
                                            within the selected radius.

                                        </div>

                                    )}


                                {analysis &&
                                    nearbyCyclones.length > 0 && (

                                        <div className="cyclone-list">

                                            {nearbyCyclones.map(
                                                (cyclone, index) => (

                                                    <div
                                                        className="cyclone-item"
                                                        key={
                                                            cyclone.id ??
                                                            index
                                                        }
                                                    >

                                                        <div>

                                                            <strong>
                                                                {
                                                                    cyclone.name ||
                                                                    "UNNAMED"
                                                                }
                                                            </strong>

                                                            <div>
                                                                Distance:{" "}
                                                                {cyclone.distance_km
                                                                    ?.toFixed?.(1) ??
                                                                    cyclone.distance_km}
                                                                {" "}km
                                                            </div>

                                                        </div>


                                                        <div>

                                                            Wind:{" "}
                                                            {cyclone.wind ??
                                                                "N/A"}

                                                        </div>

                                                    </div>

                                                )
                                            )}

                                        </div>

                                    )}

                            </div>

                        </div>


                        {/* =====================================
                            RIGHT COLUMN
                        ===================================== */}

                        <div className="right-column">


                            {/* =================================
                                RISK
                            ================================= */}

                            <div className="card risk-card">

                                <div className="card-label">
                                    CURRENT ASSESSMENT
                                </div>

                                <h2>
                                    Cyclone Risk
                                </h2>


                                {!risk && (

                                    <div className="not-analyzed">
                                        Awaiting analysis
                                    </div>

                                )}


                                {risk && (

                                    <>

                                        <div
                                            className="risk-level"
                                        >
                                            {
                                                risk.level ||
                                                "UNKNOWN"
                                            }
                                        </div>


                                        <div className="risk-bar">

                                            <div
                                                className="risk-fill"
                                                style={{
                                                    width: `${Math.min(
                                                        100,
                                                        Math.max(
                                                            0,
                                                            risk.score || 0
                                                        )
                                                    )}%`,
                                                }}
                                            />

                                        </div>


                                        <div className="risk-score">

                                            {
                                                risk.score ??
                                                0
                                            }{" "}
                                            / 100

                                        </div>


                                        <p>

                                            {risk.ai_explanation ||
                                                "Risk assessment generated from the available cyclone and weather data."}

                                        </p>

                                    </>

                                )}

                            </div>


                            {/* =================================
                                WEATHER
                            ================================= */}

                            <div className="card weather-card">

                                <div className="card-label">
                                    CURRENT CONDITIONS
                                </div>

                                <h2>
                                    Weather
                                </h2>


                                {!weather && (

                                    <div className="not-analyzed">
                                        Awaiting analysis
                                    </div>

                                )}


                                {weather?.available && (

                                    <div className="weather-data">

                                        <div>

                                            <span>
                                                Temperature
                                            </span>

                                            <strong>
                                                {
                                                    weather.temperature ??
                                                    "N/A"
                                                }
                                                °C
                                            </strong>

                                        </div>


                                        <div>

                                            <span>
                                                Wind
                                            </span>

                                            <strong>
                                                {
                                                    weather.wind_speed ??
                                                    "N/A"
                                                }
                                            </strong>

                                        </div>


                                        <div>

                                            <span>
                                                Humidity
                                            </span>

                                            <strong>
                                                {
                                                    weather.relative_humidity ??
                                                    "N/A"
                                                }%
                                            </strong>

                                        </div>

                                    </div>

                                )}

                                {weather &&
                                    weather.available === false && (

                                        <div className="not-analyzed">

                                            Weather data unavailable

                                        </div>

                                    )}

                            </div>

                        </div>

                    </section>


                    {/* =========================================
                        FORECAST
                    ========================================= */}

                    <section
                        className="card forecast-section"
                        id="forecast"
                    >

                        <div className="card-label">
                            MACHINE LEARNING
                        </div>

                        <h2>
                            Cyclone Forecast
                        </h2>


                        {!forecast && (

                            <div className="not-analyzed">
                                Run an analysis to generate a forecast.
                            </div>

                        )}


                        {forecast?.available && (

                            <div className="forecast-data">

                                <div>
                                    <span>
                                        Model
                                    </span>

                                    <strong>
                                        ML Forecast
                                    </strong>
                                </div>


                                {forecast.predictions?.map(
                                    (prediction, index) => (

                                        <div
                                            className="forecast-item"
                                            key={index}
                                        >

                                            <strong>
                                                {
                                                    prediction.cyclone ||
                                                    "Cyclone"
                                                }
                                            </strong>

                                            <span>
                                                Predicted position:{" "}
                                                {
                                                    prediction.predicted_latitude
                                                }
                                                ,{" "}
                                                {
                                                    prediction.predicted_longitude
                                                }
                                            </span>

                                            <span>
                                                Predicted wind:{" "}
                                                {
                                                    prediction.predicted_wind
                                                }
                                            </span>

                                        </div>

                                    )
                                )}

                            </div>

                        )}

                    </section>


                    {/* =========================================
                        AI
                    ========================================= */}

                    <section
                        className="card ai-section"
                        id="ai"
                    >

                        <div className="card-label">
                            ARTIFICIAL INTELLIGENCE
                        </div>

                        <h2>
                            AI Analysis
                        </h2>

                        <p>

                            Your live cyclone data can be combined
                            with RAG knowledge and the local Ollama
                            model to explain the current situation.

                        </p>

                        {analysis?.ai_explanation && (

                            <div className="ai-response">

                                {analysis.ai_explanation}

                            </div>

                        )}

                    </section>

                </section>

            </main>

        </div>
    );
}

export default App;