import { useState, useEffect } from "react";
import axios from "axios";

function JournalHistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const token = localStorage.getItem("token");
        // Let's grab the last 60 days of entries for the history feed
        const res = await axios.get("http://localhost:8000/api/v1/daily-entries?days=60", {
          headers: { Authorization: `Bearer ${token}` }
        });
        setHistory(res.data);
      } catch (error) {
        console.error("Failed to load history", error);
        if (error.response && error.response.status === 401) {
          localStorage.removeItem("token");
          window.location.href = "/";
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchHistory();
  }, []);

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif", maxWidth: "800px", margin: "0 auto" }}>
      
      <div style={{ marginBottom: "30px", borderBottom: "1px solid #e2e8f0", paddingBottom: "20px" }}>
        <h2 style={{ margin: "0 0 10px 0", color: "#1e293b" }}>Journal History</h2>
        <p style={{ color: "#64748b", margin: 0 }}>Review your past entries and track your personal growth.</p>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
        {loading ? (
          <p style={{ color: "#94a3b8" }}>Loading your memories...</p>
        ) : history.length === 0 ? (
          <div style={{ backgroundColor: "#f8fafc", padding: "40px", borderRadius: "12px", textAlign: "center", border: "1px dashed #cbd5e1" }}>
            <p style={{ color: "#64748b", fontSize: "16px" }}>Your journal is currently empty.</p>
            <p style={{ color: "#94a3b8", fontSize: "14px" }}>Head over to the New Journal tab to write your first entry!</p>
          </div>
        ) : (
          history.map((item) => (
            <div key={item.id} style={{ backgroundColor: "#ffffff", padding: "25px", borderRadius: "12px", border: "1px solid #e2e8f0", boxShadow: "0 2px 4px rgba(0,0,0,0.02)" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "15px" }}>
                <span style={{ fontSize: "20px" }}>📅</span>
                <span style={{ fontWeight: "bold", color: "#475569", fontSize: "14px" }}>
                  {new Date(item.created_at || item.date).toLocaleDateString("en-US", { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
                </span>
              </div>
              <p style={{ margin: 0, color: "#334155", lineHeight: "1.7", fontSize: "15px", whiteSpace: "pre-wrap" }}>
                {item.notes || "No content written for this day."}
              </p>
            </div>
          ))
        )}
      </div>

    </div>
  );
}

export default JournalHistoryPage;