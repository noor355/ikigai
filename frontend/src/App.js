import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import AuthPage from "./pages/AuthPage";
import DashboardPage from "./pages/DashboardPage";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");

  return (
    <Router>
      <Routes>
        {/* If not logged in, show Auth Page. If logged in, redirect to Dashboard */}
        <Route 
          path="/" 
          element={!token ? <AuthPage setToken={setToken} /> : <Navigate to="/dashboard" />} 
        />
        
        {/* If logged in, show Dashboard. If not, bounce them back to Login */}
        <Route 
          path="/dashboard" 
          element={token ? <DashboardPage setToken={setToken} /> : <Navigate to="/" />} 
        />
      </Routes>
    </Router>
  );
}

export default App;