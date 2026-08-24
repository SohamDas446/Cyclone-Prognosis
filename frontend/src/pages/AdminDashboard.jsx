import { useState } from "react";
import { useAuth } from "../context/AuthContext.jsx";

const NAV_ITEMS = [
  { id: "overview", label: "Overview", icon: "▦" },
  { id: "records", label: "Cyclone records", icon: "◉" },
  { id: "upload", label: "Upload data", icon: "⇧" },
  { id: "status", label: "System status", icon: "⌁" },
];

const MOCK_RECORDS = [
  { name: "Cyclone Amphan", basin: "Bay of Bengal", updated: "2 days ago", status: "ok" },
  { name: "Cyclone Yaas", basin: "Bay of Bengal", updated: "5 days ago", status: "ok" },
  { name: "Cyclone Mocha", basin: "Bay of Bengal", updated: "Pending review", status: "pending" },
];

function Overview() {
  return (
    <div className="rise-in">
      <div className="admin-stat-grid stagger">
        <div className="admin-stat-card">
          <div className="stat-number">—</div>
          <div className="stat-label">Tracked cyclone records</div>
        </div>
        <div className="admin-stat-card">
          <div className="stat-number">—</div>
          <div className="stat-label">Pending data reviews</div>
        </div>
        <div className="admin-stat-card">
          <div className="stat-number">Live</div>
          <div className="stat-label">/live-analysis endpoint</div>
        </div>
        <div className="admin-stat-card">
          <div className="stat-number">—</div>
          <div className="stat-label">Admin API endpoints</div>
        </div>
      </div>
      <div className="card">
        <div className="card-label">DATA MANAGEMENT</div>
        <h2>Cyclone data management</h2>
        <p style={{ marginTop: 10, color: "var(--text-secondary)", fontSize: 13.5, lineHeight: 1.7 }}>
          This is where administrators would review, correct and publish the cyclone records that
          feed the live monitor, risk scoring and ML forecast. Wire this section up to real
          endpoints (e.g. <code>GET/POST /admin/cyclones</code>) once they exist on the backend.
        </p>
      </div>
    </div>
  );
}

function Records() {
  return (
    <div className="card rise-in">
      <div className="card-label">MANAGE RECORDS</div>
      <h2>Cyclone records</h2>
      <div style={{ overflowX: "auto", marginTop: 16 }}>
        <table className="admin-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Basin</th>
              <th>Last updated</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {MOCK_RECORDS.map((record) => (
              <tr key={record.name}>
                <td style={{ color: "var(--text-primary)", fontWeight: 500 }}>{record.name}</td>
                <td>{record.basin}</td>
                <td>{record.updated}</td>
                <td>
                  <span className={`status-chip ${record.status}`}>
                    {record.status === "ok" ? "Verified" : "Needs review"}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p style={{ marginTop: 16, fontSize: 12, color: "var(--text-tertiary)" }}>
        Sample rows shown for layout purposes — connect a records endpoint to make this live.
      </p>
    </div>
  );
}

function Upload() {
  return (
    <div className="card rise-in">
      <div className="card-label">DATA INGESTION</div>
      <h2>Upload / update data</h2>
      <div className="upload-zone" style={{ marginTop: 18 }}>
        <strong>Drop a cyclone dataset here</strong>
        CSV, JSON or NetCDF — disabled until an upload endpoint exists on the backend.
        <div style={{ marginTop: 16 }}>
          <button className="btn btn-ghost btn-sm" disabled>
            Choose file
          </button>
        </div>
      </div>
    </div>
  );
}

function SystemStatus() {
  const items = [
    { label: "Cyclone analysis API", detail: "http://127.0.0.1:8000/live-analysis", status: "ok" },
    { label: "Weather service", detail: "Reachable via live-analysis", status: "ok" },
    { label: "ML forecast model", detail: "Reachable via live-analysis", status: "ok" },
    { label: "Authentication API", detail: "Not yet implemented", status: "pending" },
    { label: "Admin data API", detail: "Not yet implemented", status: "pending" },
  ];
  return (
    <div className="card rise-in">
      <div className="card-label">SYSTEM STATUS</div>
      <h2>Backend connections</h2>
      <div style={{ marginTop: 16, display: "flex", flexDirection: "column", gap: 10 }}>
        {items.map((item) => (
          <div
            key={item.label}
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              padding: "12px 14px",
              border: "1px solid var(--border)",
              borderRadius: "var(--radius-sm)",
            }}
          >
            <div>
              <div style={{ fontSize: 13.5, fontWeight: 500 }}>{item.label}</div>
              <div style={{ fontSize: 11.5, color: "var(--text-tertiary)", fontFamily: "var(--font-mono)" }}>
                {item.detail}
              </div>
            </div>
            <span className={`status-chip ${item.status}`}>
              {item.status === "ok" ? "Connected" : "Pending"}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

function AdminDashboard() {
  const { user } = useAuth();
  const [active, setActive] = useState("overview");

  return (
    <div className="admin-shell">
      <aside className="admin-sidebar">
        <div className="admin-sidebar-label">ADMIN CONSOLE</div>
        {NAV_ITEMS.map((item) => (
          <button
            key={item.id}
            className={`admin-nav-item ${active === item.id ? "active" : ""}`}
            onClick={() => setActive(item.id)}
          >
            <span aria-hidden>{item.icon}</span>
            {item.label}
          </button>
        ))}
      </aside>

      <div className="admin-main">
        <div className="admin-banner rise-in">
          <span>ⓘ</span>
          <span>
            <strong>Signed in as {user?.name}, administrator (demo session).</strong> This console shows
            the intended structure for managing cyclone data. It isn't connected to a real backend yet —
            no data shown here is written anywhere. Build real admin endpoints before relying on this UI.
          </span>
        </div>

        {active === "overview" && <Overview />}
        {active === "records" && <Records />}
        {active === "upload" && <Upload />}
        {active === "status" && <SystemStatus />}
      </div>
    </div>
  );
}

export default AdminDashboard;
