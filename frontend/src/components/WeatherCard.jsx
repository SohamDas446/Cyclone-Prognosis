function WeatherCard() {
  return (
    <div className="panel weather-card">

      <div className="panel-header">

        <div>
          <span className="panel-label">
            CURRENT CONDITIONS
          </span>

          <h2>
            Weather
          </h2>
        </div>

        <span className="weather-symbol">
          ☁
        </span>

      </div>

      <div className="temperature">
        27.9<span>°C</span>
      </div>

      <div className="weather-stats">

        <div>
          <span>HUMIDITY</span>
          <strong>88%</strong>
        </div>

        <div>
          <span>CLOUD COVER</span>
          <strong>53%</strong>
        </div>

        <div>
          <span>PRESSURE</span>
          <strong>1003.8 hPa</strong>
        </div>

      </div>

    </div>
  );
}

export default WeatherCard;