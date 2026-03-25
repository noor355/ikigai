import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function AuthPage({ setToken }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate(); // This is our new router tool!

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:8000/api/v1/auth/register", { email, password });
      setMessage("Success! User registered. You can now log in.");
    } catch (error) {
      setMessage(`Registration Error: ${error.response?.data?.detail || error.message}`);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:8000/api/v1/auth/login", { email, password });
      setToken(res.data.access_token);
      localStorage.setItem("token", res.data.access_token);
      navigate("/dashboard"); // Instantly warp the user to the dashboard page!
    } catch (error) {
      setMessage(`Login Error: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif", maxWidth: "800px", margin: "0 auto" }}>
      <h1 style={{ textAlign: "center" }}>Ikigai Career Discovery</h1>
      {message && <div style={{ padding: "10px", backgroundColor: "#e3f2fd", marginBottom: "20px" }}><b>Status:</b> {message}</div>}
      
      <div style={{ display: "flex", justifyContent: "space-around", flexWrap: "wrap", gap: "20px" }}>
        <form onSubmit={handleRegister} style={{ display: "flex", flexDirection: "column", width: "300px", gap: "10px", padding: "20px", border: "1px solid #ccc", borderRadius: "8px" }}>
          <h2>Create Account</h2>
          <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required style={{ padding: "8px" }} />
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required style={{ padding: "8px" }} />
          <button type="submit" style={{ padding: "10px", backgroundColor: "#28a745", color: "white", cursor: "pointer" }}>Register</button>
        </form>

        <form onSubmit={handleLogin} style={{ display: "flex", flexDirection: "column", width: "300px", gap: "10px", padding: "20px", border: "1px solid #ccc", borderRadius: "8px" }}>
          <h2>Login</h2>
          <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required style={{ padding: "8px" }} />
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required style={{ padding: "8px" }} />
          <button type="submit" style={{ padding: "10px", backgroundColor: "#007bff", color: "white", cursor: "pointer" }}>Login</button>
        </form>
      </div>
    </div>
  );
}

export default AuthPage;