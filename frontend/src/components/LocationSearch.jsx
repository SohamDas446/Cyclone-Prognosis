import { useMemo, useState } from "react";
import { suggestLocations } from "../api/locations.js";

function LocationSearch({ location, onLocationChange, onAnalyze, loading }) {
  const [focused, setFocused] = useState(false);

  const suggestions = useMemo(() => suggestLocations(location), [location]);
  const showSuggestions = focused && suggestions.length > 0;

  return (
    <div>
      <div className="location-box">
        <span className="location-icon">⌖</span>

        <div className="location-input-wrapper">
          <label htmlFor="location-input">ANALYZE LOCATION</label>
          <input
            id="location-input"
            value={location}
            onChange={(event) => onLocationChange(event.target.value)}
            onFocus={() => setFocused(true)}
            onBlur={() => setTimeout(() => setFocused(false), 120)}
            onKeyDown={(event) => {
              if (event.key === "Enter") onAnalyze();
            }}
            placeholder="Enter a city, e.g. Kolkata, Chennai..."
            autoComplete="off"
          />
        </div>

        <button className="btn btn-primary" onClick={onAnalyze} disabled={loading}>
          {loading ? "Analyzing…" : "Analyze"}
          {!loading && <span aria-hidden>→</span>}
        </button>

        {showSuggestions && (
          <div className="location-suggestions">
            {suggestions.map((loc) => (
              <button
                key={loc.name}
                onMouseDown={() => onLocationChange(loc.name)}
              >
                <span>{loc.name}</span>
                <span className="region">{loc.region}</span>
              </button>
            ))}
          </div>
        )}
      </div>

      <p className="location-fallback-note">
        Tracking coastal locations most exposed to cyclone activity. Unrecognized names fall back to Kolkata.
      </p>
    </div>
  );
}

export default LocationSearch;
