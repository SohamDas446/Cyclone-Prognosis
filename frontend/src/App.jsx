import { useState } from "react";
import "./App.css";
import "./styles/animations.css";
import "./styles/auth.css";
import "./styles/chat.css";
import "./styles/admin.css";

import { AuthProvider, useAuth } from "./context/AuthContext.jsx";
import Header from "./components/Header.jsx";
import Dashboard from "./components/Dashboard.jsx";
import AuthPage from "./pages/AuthPage.jsx";
import AdminDashboard from "./pages/AdminDashboard.jsx";

function Shell() {
  const { isAdmin, isAuthenticated } = useAuth();
  const [view, setView] = useState("dashboard"); // dashboard | login | signup | admin
  const [authRole, setAuthRole] = useState("user");

  function navigate(next) {
    if (next === "login" || next === "signup") {
      setView(next);
      return;
    }
    if (next === "admin" && !isAdmin) {
      setAuthRole("admin");
      setView("login");
      return;
    }
    setView(next);
  }

  function handleAuthSuccess(role) {
    setView(role === "admin" ? "admin" : "dashboard");
  }

  return (
    <div className="app">
      <Header view={view} onNavigate={navigate} />

      {view === "dashboard" && <Dashboard />}

      {(view === "login" || view === "signup") && (
        <AuthPage
          key={view + authRole}
          initialMode={view}
          initialRole={authRole}
          onSuccess={handleAuthSuccess}
        />
      )}

      {view === "admin" && isAuthenticated && isAdmin && <AdminDashboard />}

      {view === "admin" && (!isAuthenticated || !isAdmin) && (
        <AuthPage
          initialMode="login"
          initialRole="admin"
          onSuccess={handleAuthSuccess}
        />
      )}
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <Shell />
    </AuthProvider>
  );
}

export default App;
