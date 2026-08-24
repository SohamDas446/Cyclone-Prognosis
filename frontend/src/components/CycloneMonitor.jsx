function CycloneItem({ cyclone, index }) {
  const distance = cyclone.distance_km?.toFixed?.(1) ?? cyclone.distance_km;
  return (
    <div className="cyclone-item rise-in" style={{ animationDelay: `${index * 0.06}s` }}>
      <div>
        <div className="cyclone-item-name">
          <span className="storm-symbol" aria-hidden>◉</span>
          {cyclone.name || "UNNAMED SYSTEM"}
        </div>
        <div className="cyclone-item-meta">
          {distance != null ? `${distance} km away` : "Distance unavailable"}
        </div>
      </div>
      <div className="cyclone-item-wind">
        {cyclone.wind ? `${cyclone.wind}` : "Wind N/A"}
      </div>
    </div>
  );
}

function CycloneMonitor({ analysis, loading }) {
  const nearbyCyclones = analysis?.nearby_cyclones || [];

  return (
    <div className="card" id="monitor">
      <div className="card-header">
        <div>
          <div className="card-label">LIVE MONITOR</div>
          <h2>Cyclone Activity</h2>
        </div>
        <div className="live-badge">
          <span className="status-dot" />
          LIVE
        </div>
      </div>

      {!analysis && !loading && (
        <div className="empty-state">
          <span style={{ fontSize: 26 }}>⌖</span>
          <p>
            Click <strong>Analyze</strong> to retrieve live cyclone information for the selected location.
          </p>
        </div>
      )}

      {loading && (
        <div className="cyclone-list">
          <div className="skeleton skeleton-row" style={{ height: 62, borderRadius: 14 }} />
          <div className="skeleton skeleton-row" style={{ height: 62, borderRadius: 14 }} />
          <div className="skeleton skeleton-row" style={{ height: 62, borderRadius: 14, opacity: 0.6 }} />
        </div>
      )}

      {analysis && !loading && nearbyCyclones.length === 0 && (
        <div className="empty-state">
          <span style={{ fontSize: 26 }}>✓</span>
          <p>No nearby cyclones found within the selected radius.</p>
        </div>
      )}

      {analysis && !loading && nearbyCyclones.length > 0 && (
        <div className="cyclone-list">
          {nearbyCyclones.map((cyclone, index) => (
            <CycloneItem cyclone={cyclone} index={index} key={cyclone.id ?? index} />
          ))}
        </div>
      )}
    </div>
  );
}

export default CycloneMonitor;
