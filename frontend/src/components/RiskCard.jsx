function riskClass(level) {
  const l = (level || "").toLowerCase();
  if (l.includes("low")) return "low";
  if (l.includes("mod")) return "moderate";
  if (l.includes("high") || l.includes("sev")) return "high";
  return "unknown";
}

function RiskCard({ risk, loading }) {
  const score = Math.min(100, Math.max(0, risk?.score || 0));

  return (
    <div className="card">
      <div className="card-label">CURRENT ASSESSMENT</div>
      <h2>Cyclone Risk</h2>

      {!risk && !loading && <div className="not-analyzed">Awaiting analysis</div>}

      {loading && (
        <div style={{ marginTop: 16 }}>
          <div className="skeleton" style={{ height: 30, width: "50%", marginBottom: 14 }} />
          <div className="skeleton" style={{ height: 8, marginBottom: 14 }} />
          <div className="skeleton" style={{ height: 40 }} />
        </div>
      )}

      {risk && !loading && (
        <div className="scale-in">
          <div className={`risk-level ${riskClass(risk.level)}`}>{risk.level || "UNKNOWN"}</div>

          <div className="risk-bar">
            <div className="risk-fill" style={{ width: `${score}%` }} />
          </div>

          <div className="risk-score">{risk.score ?? 0} / 100</div>

          <p className="risk-explanation">
            {risk.ai_explanation ||
              "Risk assessment generated from the available cyclone and weather data."}
          </p>
        </div>
      )}
    </div>
  );
}

export default RiskCard;
