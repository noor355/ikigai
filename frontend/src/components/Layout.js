import { Link, Outlet, useLocation, useNavigate } from "react-router-dom";
import "./Layout.css";

function Layout({ setToken }) {
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    setToken("");
    localStorage.removeItem("token");
    navigate("/");
  };

  // Helper function to highlight the active menu item
  const isActive = (path) => location.pathname === path;

  const menuItems = [
    { name: "Dashboard", path: "/dashboard", icon: "📊" },
    { name: "Recommendations", path: "/recommendations", icon: "🎯" },
    { name: "AI Coach", path: "/chat", icon: "💬" },
    { name: "New Journal", path: "/journal", icon: "✍️" },
    { name: "Journal History", path: "/history", icon: "🕰️" },
    { name: "Personality Tests", path: "/tests", icon: "🧩" },
  ];

  return (
    <div className="layout-container">
      
      {/* Sidebar Navigation */}
      <div className="layout-sidebar">
        <h2>Ikigai</h2>
        
        <nav className="layout-nav">
          {menuItems.map((item) => (
            <Link 
              key={item.name} 
              to={item.path} 
              className={`layout-nav-link ${isActive(item.path) ? 'active' : ''}`}
            >
              <span>{item.icon}</span> {item.name}
            </Link>
          ))}
        </nav>

        <button 
          onClick={handleLogout} 
          className="layout-logout-btn"
        >
          Logout
        </button>
      </div>

      {/* Main Content Area */}
      <div className="layout-main">
        <div className="layout-main-content">
          <Outlet /> 
        </div>
      </div>
      
    </div>
  );
}

export default Layout;