const GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search";

export async function geocodeLocation(query) {
    const trimmed = query.trim();

    if (!trimmed) {
        throw new Error("Please enter a location.");
    }

    const url = new URL(GEOCODING_URL);

    url.searchParams.set("name", trimmed);
    url.searchParams.set("count", "5");
    url.searchParams.set("language", "en");
    url.searchParams.set("format", "json");

    const response = await fetch(url.toString());

    if (!response.ok) {
        throw new Error("Unable to search for this location.");
    }

    const data = await response.json();

    if (!data.results || data.results.length === 0) {
        throw new Error(`Location "${trimmed}" could not be found.`);
    }

    const result = data.results[0];

    return {
        name: result.name,
        latitude: result.latitude,
        longitude: result.longitude,
        country: result.country || "",
        countryCode: result.country_code || "",
        region: result.admin1 || "",
        timezone: result.timezone || "",
    };
}