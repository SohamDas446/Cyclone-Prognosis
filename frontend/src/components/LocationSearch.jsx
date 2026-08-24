import { useState } from "react";

function LocationSearch({
    location,
    onLocationChange,
    onAnalyze,
    loading,
}) {
    const [focused, setFocused] = useState(false);

    return (
        <div>
            <div className="location-box">

                <span className="location-icon">⊕</span>

                <div className="location-input-wrapper">

                    <label htmlFor="location-input">
                        ANALYZE LOCATION
                    </label>

                    <input
                        id="location-input"
                        value={location}
                        onChange={(event) =>
                            onLocationChange(event.target.value)
                        }
                        onFocus={() => setFocused(true)}
                        onBlur={() =>
                            setTimeout(() => setFocused(false), 120)
                        }
                        onKeyDown={(event) => {
                            if (
                                event.key === "Enter" &&
                                !loading
                            ) {
                                onAnalyze();
                            }
                        }}
                        placeholder="Enter any place, e.g. Digha, Puri, Mumbai..."
                        autoComplete="off"
                    />

                </div>

                <button
                    className="btn btn-primary"
                    onClick={onAnalyze}
                    disabled={loading || !location.trim()}
                >
                    {loading ? "Analyzing..." : "Analyze →"}
                </button>

            </div>

            {focused && location.trim() && (
                <p className="location-search-hint">
                    Press Enter or click Analyze to search this location.
                </p>
            )}
        </div>
    );
}

export default LocationSearch;