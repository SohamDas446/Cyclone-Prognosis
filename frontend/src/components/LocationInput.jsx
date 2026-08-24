function LocationInput() {
  return (
    <div className="location-card">

      <div className="location-icon">
        ⌖
      </div>

      <div className="location-info">

        <label>
          ANALYZE LOCATION
        </label>

        <input
          type="text"
          placeholder="Enter city or location..."
        />

      </div>

      <button>
        Analyze
        <span>→</span>
      </button>

    </div>
  );
}

export default LocationInput;