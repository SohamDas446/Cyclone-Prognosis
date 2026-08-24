// =============================================================
// API CLIENT
// -------------------------------------------------------------
// This is the ONLY place that talks to the FastAPI backend.
// The endpoint, method, request body shape and base URL below
// are copied exactly from the original App.jsx — nothing about
// the backend contract has changed, this file just centralizes
// what used to be an inline fetch() call.
// =============================================================

export const API_URL = "http://127.0.0.1:8000";

/**
 * Runs a live cyclone analysis for a given point.
 * Mirrors the original request exactly:
 *   POST /live-analysis
 *   { latitude, longitude, radius_km }
 */
export async function fetchLiveAnalysis({ latitude, longitude, radiusKm = 1000 }) {
  const response = await fetch(`${API_URL}/live-analysis`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      latitude,
      longitude,
      radius_km: radiusKm,
    }),
  });

  if (!response.ok) {
    throw new Error(`Backend returned ${response.status}`);
  }

  return response.json();
}

// -------------------------------------------------------------
// NOTE ON AUTHENTICATION
// -------------------------------------------------------------
// The backend does not currently expose any authentication
// endpoints. src/context/AuthContext.jsx implements a clearly
// labelled, frontend-only demo auth flow so the UI/UX and the
// role-based navigation structure can be designed now. When a
// real auth API exists, wire it up here, e.g.:
//
//   export async function loginRequest(email, password) {
//     const res = await fetch(`${API_URL}/auth/login`, { ... });
//     ...
//   }
//
// and swap the calls inside AuthContext for these functions.
// -------------------------------------------------------------

// -------------------------------------------------------------
// NOTE ON THE AI ASSISTANT
// -------------------------------------------------------------
// The backend does not currently expose a standalone chat
// endpoint — the only AI output available is the
// `ai_explanation` field returned by /live-analysis. The
// AIAssistant component builds its conversational UI on top of
// that single field rather than inventing a new endpoint. When a
// real chat endpoint exists (e.g. POST /ai/chat), plug it in
// here and swap the local "askAssistant" logic in
// AIAssistant.jsx for a real network call.
// -------------------------------------------------------------
