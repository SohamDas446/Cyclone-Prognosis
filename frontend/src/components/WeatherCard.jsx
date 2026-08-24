function WeatherCard({ weather, loading }) {
  return (
    <div className="card">
      <div className="card-label">CURRENT CONDITIONS</div>
      <h2>Weather</h2>

      {!weather && !loading && <div className="not-analyzed">Awaiting analysis</div>}

      {loading && (
        <div className="weather-data" style={{ marginTop: 16 }}>
          <div className="skeleton" style={{ height: 44 }} />
          <div className="skeleton" style={{ height: 44 }} />
          <div className="skeleton" style={{ height: 44 }} />
        </div>
      )}

      {weather?.available && !loading && (
        <div className="weather-data scale-in">
          <div>
            <span>TEMPERATURE</span>
            <strong>{weather.temperature ?? "N/A"}°C</strong>
          </div>
          <div>
            <span>WIND</span>
            <strong>{weather.wind_speed ?? "N/A"}</strong>
          </div>
          <div>
            <span>HUMIDITY</span>
            <strong>{weather.relative_humidity ?? "N/A"}%</strong>
          </div>
        </div>
      )}

      {weather && weather.available === false && !loading && (
        <div className="not-analyzed">Weather data unavailable for this location.</div>
      )}
    </div>
  );
}

export default WeatherCard;
