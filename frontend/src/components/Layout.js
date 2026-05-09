import { Link, Outlet, useLocation, useNavigate } from "react-router-dom";
import { FiHome, FiStar, FiMessageCircle, FiFileText, FiClock, FiZap, FiLogOut } from "react-icons/fi";
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
    { name: "Dashboard", path: "/dashboard", icon: FiHome },
    { name: "Recommendations", path: "/recommendations", icon: FiStar },
    { name: "AI Coach", path: "/chat", icon: FiMessageCircle },
    { name: "New Journal", path: "/journal", icon: FiFileText },
    { name: "Journal History", path: "/history", icon: FiClock },
  ];

  return (
    <div className="layout-container">
      
      {/* Sidebar Navigation */}
      <div className="layout-sidebar">
        <h2>Ikigai</h2>
        
        <nav className="layout-nav">
          {menuItems.map((item) => {
            const IconComponent = item.icon;
            return (
              <Link 
                key={item.name} 
                to={item.path} 
                className={`layout-nav-link ${isActive(item.path) ? 'active' : ''}`}
              >
                <IconComponent size={20} />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>

        <button 
          onClick={handleLogout} 
          className="layout-logout-btn"
        >
          <FiLogOut size={20} />
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