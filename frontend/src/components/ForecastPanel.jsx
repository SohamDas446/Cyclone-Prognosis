function ForecastPanel({ forecast, loading }) {
  return (
    <section className="card forecast-section" id="forecast">
      <div className="card-label">MACHINE LEARNING</div>
      <h2>Cyclone Forecast</h2>

      {!forecast && !loading && (
        <div className="not-analyzed">Run an analysis to generate a forecast.</div>
      )}

      {loading && (
        <div className="forecast-track">
          <div className="skeleton" style={{ width: 140, height: 78, flex: "none" }} />
          <div className="skeleton" style={{ width: 140, height: 78, flex: "none" }} />
          <div className="skeleton" style={{ width: 140, height: 78, flex: "none", opacity: 0.6 }} />
        </div>
      )}

      {forecast?.available && !loading && (
        <div className="forecast-track stagger">
          {(forecast.predictions || []).map((prediction, index) => (
            <div key={index} style={{ display: "contents" }}>
              {index > 0 && <div className="forecast-connector" aria-hidden />}
              <div className="forecast-node">
                <span className="forecast-time">
                  {prediction.cyclone || `STEP ${index + 1}`}
                </span>
                <strong>
                  {prediction.predicted_latitude}, {prediction.predicted_longitude}
                </strong>
                <span className="forecast-wind">
                  Predicted wind: {prediction.predicted_wind ?? "N/A"}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {forecast && !forecast.available && !loading && (
        <div className="not-analyzed">No forecast is available for this analysis.</div>
      )}
    </section>
  );
}

export default ForecastPanel;
