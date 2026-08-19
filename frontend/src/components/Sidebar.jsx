import { NavLink } from "react-router-dom";
import { useState } from "react";

import "./Sidebar.css";

function Sidebar() {

  const [collapsed, setCollapsed] = useState(false);

  const menuItems = [
    {
      path: "/",
      icon: "▣",
      label: "Dashboard"
    },
    {
      path: "/attack",
      icon: "⚔",
      label: "Attack Simulator"
    },
    {
      path: "/defense",
      icon: "🛡",
      label: "Defense Pipeline"
    },
    {
      path: "/analytics",
      icon: "▥",
      label: "Analytics"
    },
    {
      path: "/logs",
      icon: "◉",
      label: "Live Logs"
    },
    {
      path: "/reports",
      icon: "▤",
      label: "Reports"
    },
    {
      path: "/admin",
      icon: "⚙",
      label: "Admin Panel"
    }
  ];

  return (
    <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>

      {/* HEADER */}
      <div className="sidebar-header">

        <div className="brand">

          <div className="brand-logo">
            🛡
          </div>

          <div className="brand-text">

            <div className="brand-name">
              LLM SHIELD
            </div>

            <div className="brand-subtitle">
              SECURITY LAB
            </div>

          </div>

        </div>

        <button
          className="sidebar-toggle"
          onClick={() => setCollapsed(!collapsed)}
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          ☰
        </button>

      </div>


      {/* SECTION TITLE */}

      {!collapsed && (
        <div className="sidebar-section">
          SECURITY CONSOLE
        </div>
      )}


      {/* MENU */}

      <nav className="sidebar-menu">

        {menuItems.map((item) => (

          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === "/"}
            className={({ isActive }) =>
              `sidebar-link ${isActive ? "active" : ""}`
            }
            title={collapsed ? item.label : ""}
          >

            <span className="sidebar-icon">
              {item.icon}
            </span>

            {!collapsed && (
              <span className="sidebar-label">
                {item.label}
              </span>
            )}

          </NavLink>

        ))}

      </nav>


      {/* BOTTOM STATUS */}

      <div className="sidebar-bottom">

        {!collapsed && (

          <div className="system-status">

            <span className="status-dot"></span>

            <div>

              <div className="status-title">
                SYSTEM ONLINE
              </div>

              <div className="status-text">
                All services operational
              </div>

            </div>

          </div>

        )}

        {collapsed && (
          <div
            className="collapsed-status"
            title="System Online"
          >
            <span className="status-dot"></span>
          </div>
        )}

        {!collapsed && (
          <div className="sidebar-version">
            LLM Shield v1.0.0
          </div>
        )}

      </div>

    </aside>
  );
}

export default Sidebar;