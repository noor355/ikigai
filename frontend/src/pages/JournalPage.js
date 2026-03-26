import { useState } from "react";
import axios from "axios";

function JournalPage() {
  const [formData, setFormData] = useState({
    activities: "",
    learnings: "",
    challenges: "",
    mood: "Good"
  });
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus("");

    try {
      const token = localStorage.getItem("token");
      
      // The backend expects 'activities' as a list of strings. 
      // This turns a comma-separated string ("coding, reading") into an array (["coding", "reading"])
      const payload = {
        ...formData,
        activities: formData.activities.split(",").map(item => item.trim()).filter(item => item !== "")
      };

      // Sending the journal entry to your FastAPI backend
      await axios.post("http://localhost:8000/api/v1/daily-entries", payload, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setStatus("✨ Journal entry saved securely. Your AI coach will remember this.");
      setFormData({ activities: "", learnings: "", challenges: "", mood: "Good" }); // Clear the form
    } catch (error) {
      console.error(error);
      setStatus("❌ Error saving entry. Make sure your backend server is running!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif", maxWidth: "800px", margin: "0 auto" }}>
      
      <div style={{ marginBottom: "30px" }}>
        <h2 style={{ margin: "0 0 10px 0" }}>Daily Journal</h2>
        <p style={{ color: "#6c757d", margin: 0 }}>Log your day. Your AI coach uses this to discover what truly drives you.</p>
      </div>

      <div style={{ backgroundColor: "#ffffff", padding: "30px", borderRadius: "12px", border: "1px solid #e2e8f0", boxShadow: "0 1px 3px rgba(0,0,0,0.05)" }}>
        
        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
          
          {/* Mood Selector */}
          <div>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: "bold", color: "#334155" }}>How are you feeling today?</label>
            <select 
              name="mood" 
              value={formData.mood} 
              onChange={handleChange}
              style={{ padding: "10px", width: "100%", borderRadius: "6px", border: "1px solid #cbd5e1", backgroundColor: "#f8fafc" }}
            >
              <option value="Excellent">🚀 Excellent - Highly Energized</option>
              <option value="Good">😊 Good - Steady and Productive</option>
              <option value="Neutral">😐 Neutral - Just another day</option>
              <option value="Stressed">😰 Stressed - Overwhelmed</option>
              <option value="Drained">🔋 Drained - Completely exhausted</option>
            </select>
          </div>

          {/* Activities */}
          <div>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: "bold", color: "#334155" }}>What did you actually do today?</label>
            <p style={{ fontSize: "12px", color: "#64748b", margin: "0 0 8px 0" }}>Separate tasks with commas (e.g., coding, meetings, design, writing)</p>
            <input 
              type="text" 
              name="activities" 
              value={formData.activities} 
              onChange={handleChange}
              placeholder="e.g., answered emails, built a React component, team sync..."
              style={{ padding: "10px", width: "100%", borderRadius: "6px", border: "1px solid #cbd5e1" }}
              required
            />
          </div>

          {/* Learnings */}
          <div>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: "bold", color: "#334155" }}>What did you learn or enjoy?</label>
            <textarea 
              name="learnings" 
              rows="3"
              value={formData.learnings} 
              onChange={handleChange}
              placeholder="I really enjoyed figuring out how to..."
              style={{ padding: "10px", width: "100%", borderRadius: "6px", border: "1px solid #cbd5e1", fontFamily: "inherit" }}
            />
          </div>

          {/* Challenges */}
          <div>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: "bold", color: "#334155" }}>What drained you or felt frustrating?</label>
            <textarea 
              name="challenges" 
              rows="3"
              value={formData.challenges} 
              onChange={handleChange}
              placeholder="I felt stuck when..."
              style={{ padding: "10px", width: "100%", borderRadius: "6px", border: "1px solid #cbd5e1", fontFamily: "inherit" }}
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            style={{ 
              padding: "12px", 
              backgroundColor: loading ? "#94a3b8" : "#0ea5e9", 
              color: "white", 
              border: "none", 
              borderRadius: "6px", 
              cursor: loading ? "not-allowed" : "pointer",
              fontWeight: "bold",
              marginTop: "10px"
            }}
          >
            {loading ? "Saving..." : "Save Journal Entry"}
          </button>

          {/* Success/Error Message */}
          {status && (
            <div style={{ padding: "15px", backgroundColor: status.includes("Error") ? "#fee2e2" : "#dcfce7", color: status.includes("Error") ? "#991b1b" : "#166534", borderRadius: "6px", textAlign: "center" }}>
              {status}
            </div>
          )}

        </form>
      </div>
    </div>
  );
}

export default JournalPage;