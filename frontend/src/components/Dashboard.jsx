import { useState } from "react";
import RadarGlyph from "./RadarGlyph.jsx";
import LocationSearch from "./LocationSearch.jsx";
import CycloneMonitor from "./CycloneMonitor.jsx";
import RiskCard from "./RiskCard.jsx";
import WeatherCard from "./WeatherCard.jsx";
import ForecastPanel from "./ForecastPanel.jsx";
import AIAssistant from "./AIAssistant.jsx";
import { fetchLiveAnalysis } from "../api/client.js";
import { geocodeLocation } from "../api/locations.js";

const STATS = [
    { number: "24/7", label: "Live monitoring" },
    { number: "1000km", label: "Default scan radius" },
    { number: "ML", label: "Powered forecasting" },
    { number: "RAG+AI", label: "Situation analysis" },
];

function Dashboard() {
    const [location, setLocation] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [analysis, setAnalysis] = useState(null);

    const analyzeLocation = async () => {
        const query = location.trim();

        if (!query) {
            setError("Please enter a location.");
            return;
        }

        setLoading(true);
        setError("");

        try {
            // Convert the place name into latitude and longitude.
            const target = await geocodeLocation(query);

            // Show the resolved place name in the search box.
            setLocation(target.name);

            // Send the coordinates to the cyclone analysis backend.
            const data = await fetchLiveAnalysis({
                latitude: target.latitude,
                longitude: target.longitude,
                radiusKm: 1000,
            });

            // Keep the resolved location together with the analysis.
            setAnalysis({
                ...data,
                location: {
                    name: target.name,
                    region: target.region,
                    country: target.country,
                    latitude: target.latitude,
                    longitude: target.longitude,
                },
            });
        } catch (err) {
            console.error(err);

            setAnalysis(null);

            setError(
                err?.message ||
                "Could not analyze this location."
            );
        } finally {
            setLoading(false);
        }
    };

    const risk = analysis?.risk;
    const weather = analysis?.weather;
    const forecast = analysis?.forecast;

    return (
        <main>
            <section className="hero">
                <div className="hex-field" />

                <div className="container hero-inner">
                    <div className="hero-copy rise-in">
                        <div className="eyebrow">
                            INTELLIGENT CYCLONE MONITORING
                        </div>

                        <h1>
                            Understand the storm.
                            <br />
                            <span className="accent-text">
                                Stay ahead.
                            </span>
                        </h1>

                        <p>
                            Real-time cyclone intelligence powered by
                            weather data, machine learning, satellite
                            imagery and AI.
                        </p>

                        <LocationSearch
                            location={location}
                            onLocationChange={setLocation}
                            onAnalyze={analyzeLocation}
                            loading={loading}
                        />

                        {error && (
                            <div className="error-message rise-in">
                                {error}
                            </div>
                        )}

                        {analysis?.location && !error && (
                            <p className="location-fallback-note">
                                Analyzing{" "}
                                <strong>
                                    {analysis.location.name}
                                </strong>
                                {analysis.location.region
                                    ? `, ${analysis.location.region}`
                                    : ""}
                                {analysis.location.country
                                    ? `, ${analysis.location.country}`
                                    : ""}
                                {" — "}
                                {Number(
                                    analysis.location.latitude
                                ).toFixed(4)}
                                °,{" "}
                                {Number(
                                    analysis.location.longitude
                                ).toFixed(4)}
                                °
                            </p>
                        )}

                        <div className="stats-row stagger">
                            {STATS.map((stat) => (
                                <div
                                    className="stat-block"
                                    key={stat.label}
                                >
                                    <div className="stat-number">
                                        {stat.number}
                                    </div>

                                    <div className="stat-label">
                                        {stat.label}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="hero-radar-wrap fade-in">
                        <RadarGlyph size={280} />
                    </div>
                </div>
            </section>

            <div className="container">
                <section className="dashboard">
                    <CycloneMonitor
                        analysis={analysis}
                        loading={loading}
                    />

                    <div className="right-column">
                        <RiskCard
                            risk={risk}
                            loading={loading}
                        />

                        <WeatherCard
                            weather={weather}
                            loading={loading}
                        />
                    </div>
                </section>

                <ForecastPanel
                    forecast={forecast}
                    loading={loading}
                />

                <AIAssistant
                    analysis={analysis}
                    hasAnalyzed={!!analysis}
                />
            </div>

            <div style={{ height: 60 }} />
        </main>
    );
}

export default Dashboard;