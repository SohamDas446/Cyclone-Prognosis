import { useState } from "react";
import RadarGlyph from "./RadarGlyph.jsx";
import LocationSearch from "./LocationSearch.jsx";
import CycloneMonitor from "./CycloneMonitor.jsx";
import RiskCard from "./RiskCard.jsx";
import WeatherCard from "./WeatherCard.jsx";
import ForecastPanel from "./ForecastPanel.jsx";
import AIAssistant from "./AIAssistant.jsx";
import { fetchLiveAnalysis } from "../api/client.js";
import { findLocation, DEFAULT_LOCATION } from "../api/locations.js";

const STATS = [
  { number: "24/7", label: "Live monitoring" },
  { number: "1000km", label: "Default scan radius" },
  { number: "ML", label: "Powered forecasting" },
  { number: "RAG+AI", label: "Situation analysis" },
];

function Dashboard() {
  const [location, setLocation] = useState(DEFAULT_LOCATION.name);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [usedFallback, setUsedFallback] = useState(false);

  const analyzeLocation = async () => {
    setLoading(true);
    setError("");

    try {
      const match = findLocation(location);
      const target = match || DEFAULT_LOCATION;
      setUsedFallback(!match);

      const data = await fetchLiveAnalysis({
        latitude: target.latitude,
        longitude: target.longitude,
        radiusKm: 1000,
      });

      setAnalysis(data);
    } catch (err) {
      console.error(err);
      setError("Could not connect to the cyclone analysis server. Is the backend running on port 8000?");
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
            <div className="eyebrow">INTELLIGENT CYCLONE MONITORING</div>
            <h1>
              Understand the storm.
              <br />
              <span className="accent-text">Stay ahead.</span>
            </h1>
            <p>
              Real-time cyclone intelligence powered by weather data, machine learning, satellite
              imagery and AI.
            </p>

            <LocationSearch
              location={location}
              onLocationChange={setLocation}
              onAnalyze={analyzeLocation}
              loading={loading}
            />

            {error && <div className="error-message rise-in">{error}</div>}

            {usedFallback && analysis && !error && (
              <p className="location-fallback-note">
                Showing results for {DEFAULT_LOCATION.name} — "{location}" isn't in the tracked location list yet.
              </p>
            )}

            <div className="stats-row stagger">
              {STATS.map((stat) => (
                <div className="stat-block" key={stat.label}>
                  <div className="stat-number">{stat.number}</div>
                  <div className="stat-label">{stat.label}</div>
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
          <CycloneMonitor analysis={analysis} loading={loading} />

          <div className="right-column">
            <RiskCard risk={risk} loading={loading} />
            <WeatherCard weather={weather} loading={loading} />
          </div>
        </section>

        <ForecastPanel forecast={forecast} loading={loading} />
        <AIAssistant analysis={analysis} hasAnalyzed={!!analysis} />
      </div>

      <div style={{ height: 60 }} />
    </main>
  );
}

export default Dashboard;
