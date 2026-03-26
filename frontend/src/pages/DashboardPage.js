function DashboardPage() {
  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif", maxWidth: "1000px", margin: "0 auto" }}>
      
      {/* Header section */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "30px" }}>
        <h2>Dashboard</h2>
      </div>

      {/* Welcome Banner */}
      <div style={{ backgroundColor: "#e0f2fe", padding: "30px", borderRadius: "12px", marginBottom: "30px", border: "1px solid #bae6fd" }}>
        <h3 style={{ margin: "0 0 10px 0", color: "#0369a1" }}>Welcome to your Ikigai Command Center! 🚀</h3>
        <p style={{ margin: 0, color: "#0c4a6e" }}>
          This is where your AI Coach will soon display your personalized career insights, journal streaks, and personality growth metrics.
        </p>
      </div>

      {/* Placeholder Grid for Future Data */}
      <div style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>
        
        {/* Placeholder Card 1 */}
        <div style={{ flex: "1 1 300px", backgroundColor: "#f8f9fa", padding: "20px", borderRadius: "8px", border: "1px solid #dee2e6" }}>
          <h4 style={{ marginTop: 0, color: "#495057" }}>Weekly AI Insight</h4>
          <p style={{ color: "#6c757d", fontSize: "14px" }}>Start chatting with your AI coach or write a journal entry to generate your first insight.</p>
        </div>

        {/* Placeholder Card 2 */}
        <div style={{ flex: "1 1 300px", backgroundColor: "#f8f9fa", padding: "20px", borderRadius: "8px", border: "1px solid #dee2e6" }}>
          <h4 style={{ marginTop: 0, color: "#495057" }}>Recent Activity</h4>
          <p style={{ color: "#6c757d", fontSize: "14px" }}>No recent journal entries. Log your daily activities to feed the AI's memory.</p>
        </div>

      </div>

    </div>
  );
}

export default DashboardPage;