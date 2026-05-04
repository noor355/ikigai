import { useState, useEffect } from "react";
import axios from "axios";
import { FiTrendingUp, FiInfo, FiActivity, FiLoader } from "react-icons/fi";
import { MdAutoAwesome } from "react-icons/md";
import './DashboardPage.css';
import heroImage from '../assets/illustrations/heroikigai.jpg';

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

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="dashboard-container">
          <div className="loading-container">
            <div className="loading-spinner">
              <FiLoader />
            </div>
            <p>Loading your Dashboard...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <div className="dashboard-container">
        
        {/* Hero Section */}
        <div className="dashboard-hero">
          <div className="hero-image-container">
            <img 
              src={heroImage}
              alt="Welcome to Ikigai"
              className="hero-image"
            />
          </div>
          <div className="hero-content">
            <h1>Ikigai, your career compass</h1>
            <p className="hero-tagline">Journal your days. Discover your direction</p>
            <p className="hero-subtitle">Ikigai turns self-reflection into a career roadmap</p>
          </div>
        </div>

        {/* Dashboard Grid */}
        <div className="dashboard-grid">
        
        {/* Ikigai Scores Card */}
        <div className="dashboard-card">
          <div className="card-header">
            <h4>
              <FiTrendingUp className="card-icon" />
              Ikigai Snapshot
            </h4>
          </div>
          <div className="card-body">
            <div className="card-data">
              {[
                { label: "Passion", key: "passion_score", emoji: "❤️", colorClass: "passion" },
                { label: "Skills", key: "skills_score", emoji: "⚙️", colorClass: "skills" },
                { label: "Values", key: "values_score", emoji: "🎯", colorClass: "values" },
                { label: "Readiness", key: "market_readiness", emoji: "🚀", colorClass: "readiness" }
              ].map(item => (
                <div key={item.key} className="score-item">
                  <div className="score-header">
                    <span className="score-label">
                      {item.emoji} {item.label}
                    </span>
                    <span className="score-percentage">{Math.round(analysis?.[item.key] || 0)}%</span>
                  </div>
                  <div className="score-bar">
                    <div 
                      className={`score-fill ${item.colorClass}`}
                      style={{ width: `${analysis?.[item.key] || 0}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* AI Career Insight Card */}
        <div className="dashboard-card">
          <div className="card-header">
            <h4>
              <FiInfo className="card-icon" />
              AI Insight
            </h4>
          </div>
          <div className="card-body">
            <div className="card-data">
              {recentEntries.length > 0 ? (
                <div className="ai-insight-highlight">
                  <p className="ai-insight-text">
                    Based on your recent activities like <b>{recentEntries[0].activities.slice(0, 2).join(", ")}</b>, 
                    your skills score has reached <b>{analysis?.skills_score?.toFixed(0)}%</b>. 
                    Keep exploring <b>{analysis?.passion_keywords?.slice(0, 2).join(" & ")}</b> to boost your passion alignment!
                  </p>
                </div>
              ) : (
                <div className="empty-state">
                  <p className="empty-state-text">
                    Start journaling or chatting with the AI coach to generate your first set of career insights.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Recent Journaling Activity */}
        <div className="dashboard-card">
          <div className="card-header">
            <h4>
              <FiActivity className="card-icon" />
              Latest Activity
            </h4>
          </div>
          <div className="card-body">
            <div className="card-data">
              {recentEntries.length > 0 ? (
                <ul className="activity-list">
                  {recentEntries.map((entry, i) => (
                    <li key={i} className="activity-item">
                      <span className="activity-date">
                        {new Date(entry.date).toLocaleDateString()}
                      </span>
                      <span className="activity-text">
                        {entry.activities.slice(0, 2).join(", ")}...
                      </span>
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="empty-state">
                  <p className="empty-state-text">No recent activity found.</p>
                </div>
              )}
            </div>
          </div>
        </div>

      </div>

      </div>
    </div>
  );
}

export default DashboardPage;