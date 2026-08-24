// =============================================================
// LOCATION LOOKUP (frontend-only, no backend change)
// -------------------------------------------------------------
// The original app hardcoded Kolkata's coordinates regardless of
// what the user typed. The backend has no geocoding endpoint, so
// rather than inventing one, this is a small static lookup of
// cyclone-prone coastal locations relevant to this project. If a
// typed location doesn't match, we fall back to Kolkata exactly
// like the original app did, and say so in the UI.
// =============================================================

export const KNOWN_LOCATIONS = [
  { name: "Kolkata", region: "West Bengal, India", latitude: 22.5726, longitude: 88.3639 },
  { name: "Chennai", region: "Tamil Nadu, India", latitude: 13.0827, longitude: 80.2707 },
  { name: "Visakhapatnam", region: "Andhra Pradesh, India", latitude: 17.6868, longitude: 83.2185 },
  { name: "Bhubaneswar", region: "Odisha, India", latitude: 20.2961, longitude: 85.8245 },
  { name: "Mumbai", region: "Maharashtra, India", latitude: 19.076, longitude: 72.8777 },
  { name: "Kochi", region: "Kerala, India", latitude: 9.9312, longitude: 76.2673 },
  { name: "Puri", region: "Odisha, India", latitude: 19.8135, longitude: 85.8312 },
  { name: "Paradip", region: "Odisha, India", latitude: 20.3167, longitude: 86.6167 },
  { name: "Dhaka", region: "Bangladesh", latitude: 23.8103, longitude: 90.4125 },
  { name: "Yangon", region: "Myanmar", latitude: 16.8409, longitude: 96.1735 },
];

export const DEFAULT_LOCATION = KNOWN_LOCATIONS[0];

export function findLocation(query) {
  const q = query.trim().toLowerCase();
  if (!q) return null;
  return (
    KNOWN_LOCATIONS.find((loc) => loc.name.toLowerCase() === q) ||
    KNOWN_LOCATIONS.find((loc) => loc.name.toLowerCase().startsWith(q)) ||
    null
  );
}

export function suggestLocations(query, limit = 5) {
  const q = query.trim().toLowerCase();
  if (!q) return [];
  return KNOWN_LOCATIONS.filter((loc) => loc.name.toLowerCase().includes(q)).slice(0, limit);
}
