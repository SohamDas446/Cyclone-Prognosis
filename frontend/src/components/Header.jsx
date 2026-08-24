function Header() {
  return (
    <header className="header">

      <div className="logo">

        <div className="logo-mark">
          ◌
        </div>

        <div>
          <strong>CYCLONE</strong>
          <span>PROGNOSIS</span>
        </div>

      </div>

      <nav>
        <a href="#monitor">Monitor</a>
        <a href="#forecast">Forecast</a>
        <a href="#ai">AI Analysis</a>
      </nav>

      <div className="status">
        <span className="status-dot"></span>
        SYSTEM ONLINE
      </div>

    </header>
  );
}

export default Header;