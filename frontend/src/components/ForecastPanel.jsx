function ForecastPanel() {
  return (
    <div className="forecast-panel">

      <div className="forecast-item">

        <span className="forecast-time">
          NOW
        </span>

        <strong>
          23.1°N
        </strong>

        <span>
          85.5°E
        </span>

      </div>


      <div className="forecast-line">
        <span></span>
        <span></span>
        <span></span>
      </div>


      <div className="forecast-item">

        <span className="forecast-time">
          +6 HOURS
        </span>

        <strong>
          22.7°N
        </strong>

        <span>
          85.1°E
        </span>

      </div>


      <div className="forecast-line">
        <span></span>
        <span></span>
        <span></span>
      </div>


      <div className="forecast-item">

        <span className="forecast-time">
          +12 HOURS
        </span>

        <strong>
          22.3°N
        </strong>

        <span>
          84.7°E
        </span>

      </div>

    </div>
  );
}

export default ForecastPanel;