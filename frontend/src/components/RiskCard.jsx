function RiskCard() {
  return (
    <div className="panel risk-card">

      <div className="panel-header">

        <div>
          <span className="panel-label">
            CURRENT ASSESSMENT
          </span>

          <h2>
            Cyclone Risk
          </h2>
        </div>

        <span className="risk-icon">
          !
        </span>

      </div>

      <div className="risk-value">
        MODERATE
      </div>

      <div className="risk-score">

        <div className="score-bar">
          <div className="score-fill"></div>
        </div>

        <span>
          40 / 100
        </span>

      </div>

      <p className="card-description">
        Current conditions indicate a moderate
        level of cyclone-related risk in the
        selected area.
      </p>

    </div>
  );
}

export default RiskCard;