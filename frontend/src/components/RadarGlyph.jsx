// The recurring visual signature of the product: a meteorological
// radar sweep drawn as concentric rings with a rotating sweep arm.
// Used at three scales: small (logo mark), medium (loading state),
// large (hero / auth branding panel ambient graphic).

function RadarGlyph({ size = 160, className = "" }) {
  return (
    <svg
      className={`radar-glyph ${className}`}
      width={size}
      height={size}
      viewBox="0 0 200 200"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label="Cyclone radar glyph"
    >
      <circle cx="100" cy="100" r="98" className="radar-ring radar-ring--outer" />
      <circle cx="100" cy="100" r="70" className="radar-ring" />
      <circle cx="100" cy="100" r="42" className="radar-ring" />
      <line x1="100" y1="2" x2="100" y2="198" className="radar-cross" />
      <line x1="2" y1="100" x2="198" y2="100" className="radar-cross" />

      <g className="radar-sweep">
        <path
          d="M100 100 L100 2 A98 98 0 0 1 169.3 30.7 Z"
          fill="url(#radarSweepGradient)"
        />
      </g>

      <g className="radar-spiral">
        <path
          d="M100 100 
             m 0 -34 
             a 34 34 0 1 1 -24 58 
             a 22 22 0 1 1 16 -37 
             a 11 11 0 1 1 -8 18"
          className="radar-spiral-path"
        />
      </g>

      <circle cx="100" cy="100" r="5" className="radar-core" />

      <defs>
        <linearGradient id="radarSweepGradient" x1="100" y1="2" x2="169" y2="31" gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor="var(--accent)" stopOpacity="0.55" />
          <stop offset="1" stopColor="var(--accent)" stopOpacity="0" />
        </linearGradient>
      </defs>
    </svg>
  );
}

export default RadarGlyph;
