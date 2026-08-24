function CycloneCard({
  name,
  category,
  distance,
  wind,
  pressure
}) {
  return (
    <div className="cyclone-card">

      <div className="cyclone-card-top">

        <div className="storm-symbol">
          ◉
        </div>

        <span>
          {category}
        </span>

      </div>

      <h3>
        {name}
      </h3>

      <div className="cyclone-details">

        <div>
          <span>DISTANCE</span>
          <strong>{distance}</strong>
        </div>

        <div>
          <span>WIND</span>
          <strong>{wind}</strong>
        </div>

        <div>
          <span>PRESSURE</span>
          <strong>{pressure}</strong>
        </div>

      </div>

    </div>
  );
}

export default CycloneCard;