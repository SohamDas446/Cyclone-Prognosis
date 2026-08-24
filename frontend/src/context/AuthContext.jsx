import { createContext, useContext, useEffect, useMemo, useState } from "react";

// =============================================================
// AUTH CONTEXT — FRONTEND DEMO ONLY
// -------------------------------------------------------------
// IMPORTANT: The backend does not currently expose authentication
// endpoints. This context exists so the UI, UX and role-based
// navigation structure can be designed and demonstrated now.
//
// It is NOT secure:
//   - "Passwords" are never sent anywhere or verified server-side.
//   - Anyone can open devtools and set an admin session.
//   - This must be replaced with real server-issued sessions/JWTs
//     before this app handles anything real.
//
// Every screen that reads `role === "admin"` is a UI convenience,
// not an access-control boundary. Swap loginUser/loginAdmin/signup
// below for real calls to API_URL + "/auth/..." once those
// endpoints exist (see src/api/client.js for the TODO notes).
// =============================================================

const STORAGE_KEY = "cyclone-prognosis:demo-session";

const AuthContext = createContext(null);

function readStoredSession() {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => readStoredSession());

  useEffect(() => {
    if (user) {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(user));
    } else {
      window.localStorage.removeItem(STORAGE_KEY);
    }
  }, [user]);

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: !!user,
      isAdmin: user?.role === "admin",

      // Simulated network delay so the loading state in the UI has
      // something real to show — remove once wired to a real API.
      async login({ email, password, role, remember }) {
        await fakeLatency();
        if (!email || !password) {
          throw new Error("Enter your email and password.");
        }
        const nextUser = {
          name: email.split("@")[0] || "User",
          email,
          role: role === "admin" ? "admin" : "user",
          remember: !!remember,
        };
        setUser(nextUser);
        return nextUser;
      },

      async signup({ name, email, password, role }) {
        await fakeLatency();
        if (!name || !email || !password) {
          throw new Error("Fill in every field to create an account.");
        }
        if (password.length < 8) {
          throw new Error("Use a password with at least 8 characters.");
        }
        const nextUser = {
          name,
          email,
          role: role === "admin" ? "admin" : "user",
          remember: true,
        };
        setUser(nextUser);
        return nextUser;
      },

      logout() {
        setUser(null);
      },
    }),
    [user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

function fakeLatency() {
  return new Promise((resolve) => setTimeout(resolve, 650 + Math.random() * 400));
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
