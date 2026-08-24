import { useEffect, useRef, useState } from "react";
import RadarGlyph from "./RadarGlyph.jsx";
import { useAuth } from "../context/AuthContext.jsx";

function initials(name) {
  return name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

function Header({ view, onNavigate }) {
  const { user, isAuthenticated, isAdmin, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    function handleClick(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const showAnchors = view === "dashboard";

  return (
    <header className="header">
      <button className="logo" onClick={() => onNavigate("dashboard")} aria-label="Cyclone Prognosis home">
        <RadarGlyph size={36} className="logo-mark" />
        <div className="logo-text">
          <strong>CYCLONE</strong>
          <span>PROGNOSIS</span>
        </div>
      </button>

      {showAnchors && (
        <nav>
          <a href="#monitor">Monitor</a>
          <a href="#forecast">Forecast</a>
          <a href="#ai">AI Assistant</a>
        </nav>
      )}

      <div className="header-right">
        <div className="system-status">
          <span className="status-dot" />
          SYSTEM ONLINE
        </div>

        <div className="header-actions">
          {!isAuthenticated && (
            <>
              <button className="btn btn-ghost btn-sm" onClick={() => onNavigate("login")}>
                Log in
              </button>
              <button className="btn btn-primary btn-sm" onClick={() => onNavigate("signup")}>
                Sign up
              </button>
            </>
          )}

          {isAuthenticated && (
            <div className={`user-chip ${isAdmin ? "admin" : ""}`} ref={menuRef}>
              <button
                className="user-avatar"
                style={{ border: "none" }}
                onClick={() => setMenuOpen((open) => !open)}
                aria-haspopup="menu"
                aria-expanded={menuOpen}
              >
                {initials(user.name)}
              </button>
              <button
                className="user-meta"
                style={{ background: "none", border: "none", padding: 0 }}
                onClick={() => setMenuOpen((open) => !open)}
              >
                <strong>{user.name}</strong>
                <span className={`role-pill ${isAdmin ? "admin" : ""}`}>
                  {isAdmin ? "ADMINISTRATOR" : "USER"}
                </span>
              </button>

              {menuOpen && (
                <div className="user-menu" role="menu">
                  <button
                    onClick={() => {
                      onNavigate("dashboard");
                      setMenuOpen(false);
                    }}
                  >
                    Dashboard
                  </button>
                  {isAdmin && (
                    <button
                      onClick={() => {
                        onNavigate("admin");
                        setMenuOpen(false);
                      }}
                    >
                      Admin console
                    </button>
                  )}
                  <button
                    className="danger"
                    onClick={() => {
                      logout();
                      setMenuOpen(false);
                      onNavigate("dashboard");
                    }}
                  >
                    Log out
                  </button>
                </div>
              )}
            </div>
          )}

          {showAnchors && (
            <button
              className="menu-toggle"
              onClick={() => setMobileNavOpen((open) => !open)}
              aria-label="Toggle navigation"
            >
              {mobileNavOpen ? "✕" : "☰"}
            </button>
          )}
        </div>
      </div>

      {mobileNavOpen && (
        <div className="mobile-nav">
          <a href="#monitor" onClick={() => setMobileNavOpen(false)}>Monitor</a>
          <a href="#forecast" onClick={() => setMobileNavOpen(false)}>Forecast</a>
          <a href="#ai" onClick={() => setMobileNavOpen(false)}>AI Assistant</a>
        </div>
      )}
    </header>
  );
}

export default Header;
