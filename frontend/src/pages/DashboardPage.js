import { useState, useEffect } from "react";
import axios from "axios";

function DashboardPage() {
  const [analysis, setAnalysis] = useState(null);
  const [recentEntries, setRecentEntries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("token");
        const headers = { Authorization: `Bearer ${token}` };

        const [analysisRes, entriesRes] = await Promise.all([
          axios.get("http://localhost:8000/api/v1/recommendations/analysis", { headers }),
          axios.get("http://localhost:8000/api/v1/daily-entries/", { headers })
        ]);

        setAnalysis(analysisRes.data.analysis);
        setRecentEntries(entriesRes.data.slice(0, 3));
      } catch (error) {
        console.error("Dashboard data fetch error:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div style={{ padding: "40px" }}>Loading Dashboard...</div>;

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif", maxWidth: "1000px", margin: "0 auto" }}>
      
      {/* Header section */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "30px" }}>
        <h2>Dashboard</h2>
      </div>

      {/* Welcome Banner */}
      <div style={{ backgroundColor: "#e0f2fe", padding: "30px", borderRadius: "12px", marginBottom: "30px", border: "1px solid #bae6fd" }}>
        <h3 style={{ margin: "0 0 10px 0", color: "#0369a1" }}>Welcome back! 🚀</h3>
        <p style={{ margin: 0, color: "#0c4a6e" }}>
          Your profile is <b>{analysis?.profile_completeness?.toFixed(0) || 0}%</b> complete. 
          {analysis?.profile_completeness < 100 ? " Complete your profile to get more accurate career matches." : " You're all set for AI-powered discovery!"}
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: "20px" }}>
        
        {/* Ikigai Scores Card */}
        <div style={{ backgroundColor: "#ffffff", padding: "24px", borderRadius: "12px", border: "1px solid #e2e8f0", boxShadow: "0 4px 6px -1px rgba(0,0,0,0.1)" }}>
          <h4 style={{ marginTop: 0, color: "#2d3748", borderBottom: "2px solid #edf2f7", paddingBottom: "10px" }}>Ikigai Snapshot</h4>
          <div style={{ marginTop: "20px", display: "flex", flexDirection: "column", gap: "15px" }}>
            {[
              { label: "Passion", score: analysis?.passion_score, color: "#f687b3" },
              { label: "Skills", score: analysis?.skills_score, color: "#4299e1" },
              { label: "Values", score: analysis?.values_score, color: "#48bb78" },
              { label: "Readiness", score: analysis?.market_readiness, color: "#ecc94b" }
            ].map(item => (
              <div key={item.label}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "5px" }}>
                  <span style={{ fontSize: "14px", fontWeight: "600" }}>{item.label}</span>
                  <span style={{ fontSize: "14px", fontWeight: "600" }}>{Math.round(item.score || 0)}%</span>
                </div>
                <div style={{ height: "8px", backgroundColor: "#edf2f7", borderRadius: "4px", overflow: "hidden" }}>
                  <div style={{ height: "100%", width: `${item.score || 0}%`, backgroundColor: item.color, transition: "width 1s ease-in-out" }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Career Insight Card */}
        <div style={{ backgroundColor: "#ffffff", padding: "24px", borderRadius: "12px", border: "1px solid #e2e8f0", boxShadow: "0 4px 6px -1px rgba(0,0,0,0.1)" }}>
          <h4 style={{ marginTop: 0, color: "#2d3748", borderBottom: "2px solid #edf2f7", paddingBottom: "10px" }}>AI Insight</h4>
          <div style={{ marginTop: "15px" }}>
            {recentEntries.length > 0 ? (
              <p style={{ color: "#4a5568", lineHeight: "1.6" }}>
                Based on your recent activities like <b>{recentEntries[0].activities.slice(0, 2).join(", ")}</b>, 
                your skills score has reached <b>{analysis?.skills_score?.toFixed(0)}%</b>. 
                Keep exploring <b>{analysis?.passion_keywords?.slice(0, 2).join(" & ")}</b> to boost your passion alignment!
              </p>
            ) : (
              <p style={{ color: "#718096" }}>Start journaling or chatting with the AI coach to generate your first set of career insights.</p>
            )}
          </div>
        </div>

        {/* Recent Journaling Activity */}
        <div style={{ backgroundColor: "#ffffff", padding: "24px", borderRadius: "12px", border: "1px solid #e2e8f0", boxShadow: "0 4px 6px -1px rgba(0,0,0,0.1)" }}>
          <h4 style={{ marginTop: 0, color: "#2d3748", borderBottom: "2px solid #edf2f7", paddingBottom: "10px" }}>Latest Activity</h4>
          <div style={{ marginTop: "15px" }}>
            {recentEntries.length > 0 ? (
              <ul style={{ listStyle: "none", padding: 0 }}>
                {recentEntries.map((entry, i) => (
                  <li key={i} style={{ padding: "10px 0", borderBottom: i === recentEntries.length - 1 ? "none" : "1px solid #f7fafc", fontSize: "14px" }}>
                    <span style={{ color: "#718096" }}>{new Date(entry.date).toLocaleDateString()}:</span> {entry.activities.slice(0, 2).join(", ")}...
                  </li>
                ))}
              </ul>
            ) : (
              <p style={{ color: "#718096" }}>No recent activity found.</p>
            )}
          </div>
        </div>

      </div>

    </div>
  );
}

export default DashboardPage;