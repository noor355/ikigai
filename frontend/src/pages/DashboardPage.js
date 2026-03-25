import { useNavigate } from "react-router-dom";

function DashboardPage({ setToken }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    setToken("");
    localStorage.removeItem("token");
    navigate("/"); // Send them back to the login page
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif", maxWidth: "800px", margin: "0 auto", textAlign: "center" }}>
      <h2>Welcome to your Ikigai Dashboard!</h2>
      <p>This is where we will build your personalized career discovery questionnaire.</p>
      <button onClick={handleLogout} style={{ padding: "10px 20px", backgroundColor: "#dc3545", color: "white", border: "none", cursor: "pointer", borderRadius: "4px" }}>
        Logout
      </button>
    </div>
  );
}

export default DashboardPage;