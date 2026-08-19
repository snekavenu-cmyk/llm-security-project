import "./Navbar.css";

function Navbar() {

  return (

    <nav className="navbar">

      <div className="navbar-left">

        <div className="navbar-title">
          LLM Security Operations Center
        </div>

        <div className="navbar-divider"></div>

        <div className="navbar-subtitle">
          Prompt Injection Detection & Defense
        </div>

      </div>


      <div className="navbar-right">

        <div className="api-status">

          <span className="api-dot"></span>

          API ONLINE

        </div>


        <div className="admin-badge">
          ADMIN
        </div>

      </div>

    </nav>

  );

}

export default Navbar;