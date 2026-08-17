import { Link } from "react-router-dom";

import "./Sidebar.css";

function Sidebar(){

    return(

        <div className="sidebar">

            <Link to="/">Home</Link>

            <Link to="/attack">Attack Simulator</Link>

            <Link to="/defense">Defense Pipeline</Link>

            <Link to="/analytics">Analytics</Link>

            <Link to="/logs">Live Logs</Link>

            <Link to="/reports">Reports</Link>

            <Link to="/admin">Admin</Link>

        </div>

    );

}

export default Sidebar;