import { useState } from "react";
import axios from "axios";

function JournalPage() {
  const [entry, setEntry] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!entry.trim()) return;
    
    setLoading(true);
    setStatus("");

    try {
      const token = localStorage.getItem("token");
      
      // We only send 'activities' (required by the database) and 'notes' (the journal content).
      // Your Python backend will automatically handle the rest!
      const payload = {
        activities: ["Freeform Journal"],
        notes: entry
      };

      await axios.post("http://localhost:8000/api/v1/daily-entries/", payload, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setStatus("✨ Entry secured. Your AI coach is quietly analyzing this.");
      setEntry(""); // Clear the page for tomorrow
    } catch (error) {
      console.error(error);
      setStatus("❌ Error saving entry. Make sure your backend server is running!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif", maxWidth: "800px", margin: "0 auto", height: "100%" }}>
      
      <div style={{ marginBottom: "30px" }}>
        <h2 style={{ margin: "0 0 10px 0" }}>Your Journal</h2>
        <p style={{ color: "#6c757d", margin: 0 }}>
          Write about your day, your random thoughts, or anything on your mind. 
          There are no rules. Your AI uses this context to guide you later.
        </p>
      </div>

      <div style={{ backgroundColor: "#ffffff", padding: "30px", borderRadius: "12px", border: "1px solid #e2e8f0", boxShadow: "0 4px 6px -1px rgba(0,0,0,0.05)", display: "flex", flexDirection: "column", height: "60vh" }}>
        
        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", flex: 1, gap: "20px" }}>
          
          <textarea 
            value={entry} 
            onChange={(e) => setEntry(e.target.value)}
            placeholder="Dear Journal..."
            style={{ 
              flex: 1, 
              padding: "20px", 
              borderRadius: "8px", 
              border: "none", 
              backgroundColor: "#f8fafc",
              fontSize: "16px",
              lineHeight: "1.6",
              resize: "none",
              outline: "none",
              fontFamily: "inherit",
              boxShadow: "inset 0 2px 4px 0 rgba(0, 0, 0, 0.05)"
            }}
          />

          <button 
            type="submit" 
            disabled={loading || !entry.trim()}
            style={{ 
              padding: "15px", 
              backgroundColor: loading || !entry.trim() ? "#cbd5e1" : "#10b981", 
              color: "white", 
              border: "none", 
              borderRadius: "8px", 
              cursor: loading || !entry.trim() ? "not-allowed" : "pointer",
              fontWeight: "bold",
              fontSize: "16px",
              transition: "background-color 0.2s"
            }}
          >
            {loading ? "Saving to memory..." : "Save Entry"}
          </button>

          {/* Success/Error Message */}
          {status && (
            <div style={{ padding: "15px", backgroundColor: status.includes("Error") ? "#fee2e2" : "#dcfce7", color: status.includes("Error") ? "#991b1b" : "#166534", borderRadius: "8px", textAlign: "center", fontWeight: "500" }}>
              {status}
            </div>
          )}

        </form>
      </div>
    </div>
  );
}

export default JournalPage;