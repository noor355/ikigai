import { Link, Outlet, useLocation, useNavigate } from "react-router-dom";

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
    { name: "AI Coach", path: "/chat", icon: "💬" },
    { name: "Daily Journal", path: "/journal", icon: "📓" },
    { name: "Personality Tests", path: "/tests", icon: "🧩" },
  ];

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "sans-serif", backgroundColor: "#f4f7f6" }}>
      
      {/* Sidebar Navigation */}
      <div style={{ width: "250px", backgroundColor: "#1e293b", color: "white", display: "flex", flexDirection: "column", padding: "20px 0" }}>
        <h2 style={{ textAlign: "center", borderBottom: "1px solid #334155", paddingBottom: "20px", marginBottom: "20px" }}>Ikigai</h2>
        
        <nav style={{ display: "flex", flexDirection: "column", flex: 1 }}>
          {menuItems.map((item) => (
            <Link 
              key={item.name} 
              to={item.path} 
              style={{ 
                textDecoration: "none", 
                color: isActive(item.path) ? "#38bdf8" : "#cbd5e1", 
                backgroundColor: isActive(item.path) ? "#0f172a" : "transparent",
                padding: "15px 20px", 
                fontSize: "16px",
                display: "flex",
                alignItems: "center",
                gap: "10px",
                transition: "background 0.2s"
              }}
            >
              <span>{item.icon}</span> {item.name}
            </Link>
          ))}
        </nav>

        <button 
          onClick={handleLogout} 
          style={{ margin: "20px", padding: "10px", backgroundColor: "#ef4444", color: "white", border: "none", borderRadius: "6px", cursor: "pointer", fontWeight: "bold" }}
        >
          Logout
        </button>
      </div>

      {/* Main Content Area (This is where the pages load!) */}
      <div style={{ flex: 1, overflowY: "auto", padding: "20px" }}>
        <div style={{ backgroundColor: "white", borderRadius: "12px", minHeight: "90%", boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)" }}>
          {/* Outlet is the magic React Router component that swaps the pages out */}
          <Outlet /> 
        </div>
      </div>
      
    </div>
  );
}

export default Layout;