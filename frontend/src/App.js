import axios from "axios";
import { useState } from "react";

function App() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  
  // Check if a user is already logged in by looking for a saved token
  const [token, setToken] = useState(localStorage.getItem("token") || "");

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      // Registration expects standard JSON
      const res = await axios.post("http://127.0.0.1:8000/api/v1/auth/register", {
        email: email,
        username: username,
        password: password
      });
      setMessage(`Success! User ${res.data.username} registered. You can now log in.`);
    } catch (error) {
      setMessage(`Registration Error: ${error.response?.data?.detail || error.message}`);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      // Sending standard JSON to match your backend
      const res = await axios.post("http://localhost:8000/api/v1/auth/login", {
        email: email,       // Your backend probably expects 'email' or 'username' here
        password: password
      });

      // Save the token so the user stays logged in
      setToken(res.data.access_token);
      localStorage.setItem("token", res.data.access_token);
      setMessage("Logged in successfully!");
      
    } catch (error) {
      // Unpacking the 422 error so we can read it on the screen
      let errorMsg = "Login failed";
      if (error.response?.data?.detail) {
        errorMsg = typeof error.response.data.detail === "string" 
          ? error.response.data.detail 
          : JSON.stringify(error.response.data.detail);
      } else {
        errorMsg = error.message;
      }
      setMessage(`Login Error: ${errorMsg}`);
    }
  };

  const handleLogout = () => {
    setToken("");
    localStorage.removeItem("token");
    setMessage("You have been logged out.");
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif", maxWidth: "800px", margin: "0 auto" }}>
      <h1 style={{ textAlign: "center" }}>Ikigai Career Discovery</h1>
      
      {/* Status Message Display */}
      {message && (
        <div style={{ padding: "10px", backgroundColor: "#e3f2fd", marginBottom: "20px", borderRadius: "5px" }}>
          <b>Status:</b> {message}
        </div>
      )}

      {/* Conditional Rendering: Show forms if logged out, show dashboard if logged in */}
      {!token ? (
        <div style={{ display: "flex", justifyContent: "space-around", flexWrap: "wrap", gap: "20px" }}>
          
          {/* Register Form */}
          <form onSubmit={handleRegister} style={{ display: "flex", flexDirection: "column", width: "300px", gap: "10px", padding: "20px", border: "1px solid #ccc", borderRadius: "8px" }}>
            <h2>Create Account</h2>
            <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required style={{ padding: "8px" }} />
            <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required style={{ padding: "8px" }} />
            <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required style={{ padding: "8px" }} />
            <button type="submit" style={{ padding: "10px", backgroundColor: "#28a745", color: "white", border: "none", cursor: "pointer", borderRadius: "4px" }}>Register</button>
          </form>

          {/* Login Form */}
          <form onSubmit={handleLogin} style={{ display: "flex", flexDirection: "column", width: "300px", gap: "10px", padding: "20px", border: "1px solid #ccc", borderRadius: "8px" }}>
            <h2>Login</h2>
            <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required style={{ padding: "8px" }} />
            <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required style={{ padding: "8px" }} />
            <button type="submit" style={{ padding: "10px", backgroundColor: "#007bff", color: "white", border: "none", cursor: "pointer", borderRadius: "4px" }}>Login</button>
          </form>

        </div>
      ) : (
        <div style={{ textAlign: "center", padding: "40px", border: "1px solid #ccc", borderRadius: "8px" }}>
          <h2>Welcome to your Dashboard!</h2>
          <p>You are successfully authenticated and your JWT token is securely stored.</p>
          <button onClick={handleLogout} style={{ padding: "10px 20px", backgroundColor: "#dc3545", color: "white", border: "none", cursor: "pointer", borderRadius: "4px" }}>Logout</button>
        </div>
      )}
    </div>
  );
}

export default App;