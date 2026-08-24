import { useState } from "react";
import RadarGlyph from "../components/RadarGlyph.jsx";
import { useAuth } from "../context/AuthContext.jsx";

const COPY = {
  user: {
    title: "Track the storm before it tracks you.",
    body: "Search any coastal location, pull live cyclone activity, weather and machine-learning forecasts, and ask the AI assistant to explain what it means for you.",
  },
  admin: {
    title: "Keep the data behind every forecast accurate.",
    body: "The admin console is where cyclone records, data sources and system status get reviewed and updated.",
  },
};

function AuthPage({ initialMode = "login", initialRole = "user", onSuccess }) {
  const { login, signup } = useAuth();
  const [mode, setMode] = useState(initialMode); // "login" | "signup"
  const [role, setRole] = useState(initialRole); // "user" | "admin"
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(true);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (mode === "login") {
        await login({ email, password, role, remember });
      } else {
        await signup({ name, email, password, role });
      }
      setSuccess(true);
      setTimeout(() => onSuccess?.(role), 700);
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  const copy = COPY[role];

  return (
    <div className="auth-screen">
      <div className={`auth-branding ${role === "admin" ? "admin-mode" : ""}`}>
        <div className="hex-field" />
        <RadarGlyph size={380} />
        <div className="auth-branding-content rise-in">
          <div className="eyebrow" style={{ color: role === "admin" ? "var(--admin)" : "var(--accent-bright)" }}>
            CYCLONE PROGNOSIS
          </div>
          <h2>{copy.title}</h2>
          <p>{copy.body}</p>
        </div>
      </div>

      <div className="auth-form-side">
        <div className="auth-card scale-in">
          {success ? (
            <div className="auth-success">
              <div className="success-icon">✓</div>
              <h2>{mode === "login" ? "Welcome back" : "Account created"}</h2>
              <p style={{ color: "var(--text-secondary)", fontSize: 13.5 }}>
                Taking you to your {role === "admin" ? "admin console" : "dashboard"}…
              </p>
            </div>
          ) : (
            <>
              <div className="role-tabs">
                <button
                  className={role === "user" ? "active" : ""}
                  onClick={() => setRole("user")}
                  type="button"
                >
                  User
                </button>
                <button
                  className={role === "admin" ? "active admin-active" : ""}
                  onClick={() => setRole("admin")}
                  type="button"
                >
                  Administrator
                </button>
              </div>

              <div className="auth-mode-toggle">
                <button
                  type="button"
                  className={mode === "login" ? "active" : ""}
                  onClick={() => setMode("login")}
                >
                  Log in
                </button>
                <button
                  type="button"
                  className={mode === "signup" ? "active" : ""}
                  onClick={() => setMode("signup")}
                >
                  Sign up
                </button>
              </div>

              {error && <div className="auth-error">{error}</div>}

              <form onSubmit={handleSubmit} key={mode}>
                {mode === "signup" && (
                  <div className="form-field rise-in">
                    <label htmlFor="name">Full name</label>
                    <div className="input-shell">
                      <input
                        id="name"
                        value={name}
                        onChange={(event) => setName(event.target.value)}
                        placeholder="Jordan Rivera"
                        required
                      />
                    </div>
                  </div>
                )}

                <div className="form-field rise-in">
                  <label htmlFor="email">Email</label>
                  <div className="input-shell">
                    <input
                      id="email"
                      type="email"
                      value={email}
                      onChange={(event) => setEmail(event.target.value)}
                      placeholder={role === "admin" ? "you@cycloneprognosis.org" : "you@example.com"}
                      required
                    />
                  </div>
                </div>

                <div className="form-field rise-in">
                  <label htmlFor="password">Password</label>
                  <div className="input-shell">
                    <input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      value={password}
                      onChange={(event) => setPassword(event.target.value)}
                      placeholder="••••••••"
                      minLength={mode === "signup" ? 8 : undefined}
                      required
                    />
                    <button
                      type="button"
                      className="toggle-visibility"
                      onClick={() => setShowPassword((show) => !show)}
                    >
                      {showPassword ? "Hide" : "Show"}
                    </button>
                  </div>
                </div>

                {mode === "login" && (
                  <div className="form-row">
                    <label className="checkbox-field">
                      <input
                        type="checkbox"
                        checked={remember}
                        onChange={(event) => setRemember(event.target.checked)}
                      />
                      Remember me
                    </label>
                    <button type="button" className="link-btn">
                      Forgot password?
                    </button>
                  </div>
                )}

                <button className="btn btn-primary btn-block" type="submit" disabled={loading} style={{ marginTop: mode === "signup" ? 8 : 0 }}>
                  {loading
                    ? mode === "login" ? "Logging in…" : "Creating account…"
                    : mode === "login" ? "Log in" : `Create ${role} account`}
                </button>
              </form>

              <p className="auth-switch">
                {mode === "login" ? "New here?" : "Already have an account?"}{" "}
                <button className="link-btn" onClick={() => setMode(mode === "login" ? "signup" : "login")}>
                  {mode === "login" ? "Create an account" : "Log in instead"}
                </button>
              </p>

              <div className="demo-note">
                <span>ⓘ</span>
                <span>
                  <strong>Demo authentication.</strong> The backend doesn't expose auth endpoints yet, so this
                  form only builds a local session to preview the role-based UI — it isn't securing anything.
                </span>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default AuthPage;
