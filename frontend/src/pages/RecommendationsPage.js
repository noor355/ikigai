import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './RecommendationsPage.css';

const RecommendationsPage = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedCareer, setSelectedCareer] = useState(null);

  useEffect(() => {
    fetchRecommendations();
    fetchAnalysis();
  }, []);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(
        'http://localhost:8000/api/v1/recommendations/',
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      setRecommendations(response.data);
    } catch (err) {
      setError('Failed to fetch recommendations');
    } finally {
      setLoading(false);
    }
  };

  const fetchAnalysis = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(
        'http://localhost:8000/api/v1/recommendations/analysis',
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      setAnalysis(response.data.analysis);
    } catch (err) {
      console.log('Analysis fetch error:', err);
    }
  };

  const generateRecommendations = async () => {
    setLoading(true);
    setError('');
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        'http://localhost:8000/api/v1/recommendations/generate',
        { top_n: 5 },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      setRecommendations(response.data.recommendations);
      setAnalysis(response.data.user_profile_analysis);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate recommendations');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#28a745';
    if (score >= 60) return '#ffc107';
    return '#dc3545';
  };

  const getScoreBadge = (score) => {
    if (score >= 80) return 'Perfect Match';
    if (score >= 60) return 'Good Match';
    return 'Potential Match';
  };

  return (
    <div className="recommendations-page">
      <div className="recommendations-container">
        <h2>🎯 Your AI-Powered Career Recommendations</h2>
        <p className="subtitle">
          Based on your profile, daily journal entries, and Ikigai framework analysis
        </p>

        {error && <div className="error-message">{error}</div>}

        {/* Profile Analysis */}
        {analysis && (
          <div className="analysis-section">
            <h3>📊 Your Profile Analysis</h3>
            <div className="scores-grid">
              <div className="score-card">
                <label>Passion Score</label>
                <div className="score-bar">
                  <div
                    className="score-fill"
                    style={{
                      width: `${analysis.passion_score}%`,
                      backgroundColor: getScoreColor(analysis.passion_score),
                    }}
                  />
                </div>
                <span className="score-value">{Math.round(analysis.passion_score)}/100</span>
              </div>

              <div className="score-card">
                <label>Skills Score</label>
                <div className="score-bar">
                  <div
                    className="score-fill"
                    style={{
                      width: `${analysis.skills_score}%`,
                      backgroundColor: getScoreColor(analysis.skills_score),
                    }}
                  />
                </div>
                <span className="score-value">{Math.round(analysis.skills_score)}/100</span>
              </div>

              <div className="score-card">
                <label>Values Score</label>
                <div className="score-bar">
                  <div
                    className="score-fill"
                    style={{
                      width: `${analysis.values_score}%`,
                      backgroundColor: getScoreColor(analysis.values_score),
                    }}
                  />
                </div>
                <span className="score-value">{Math.round(analysis.values_score)}/100</span>
              </div>

              <div className="score-card">
                <label>Market Readiness</label>
                <div className="score-bar">
                  <div
                    className="score-fill"
                    style={{
                      width: `${analysis.market_readiness}%`,
                      backgroundColor: getScoreColor(analysis.market_readiness),
                    }}
                  />
                </div>
                <span className="score-value">{Math.round(analysis.market_readiness)}/100</span>
              </div>
            </div>
          </div>
        )}

        {/* Generate Button */}
        <div style={{ marginBottom: '24px' }}>
          <button
            onClick={generateRecommendations}
            disabled={loading}
            className="btn-generate"
          >
            {loading ? '⏳ Analyzing your profile...' : '✨ Generate Fresh Recommendations'}
          </button>
        </div>

        {/* Recommendations List */}
        {loading ? (
          <div className="loading">
            <p>🤖 AI is analyzing your data and matching careers...</p>
          </div>
        ) : recommendations.length > 0 ? (
          <div className="recommendations-list">
            {recommendations.map((rec, index) => (
              <div
                key={index}
                className="career-card"
                onClick={() => setSelectedCareer(selectedCareer === index ? null : index)}
              >
                <div className="career-header">
                  <div className="career-info">
                    <h3>{rec.career_title}</h3>
                    <p className="description">{rec.description}</p>
                  </div>
                  <div className="career-score" style={{ borderColor: getScoreColor(rec.match_score) }}>
                    <div
                      className="score-number"
                      style={{ color: getScoreColor(rec.match_score) }}
                    >
                      {Math.round(rec.match_score)}%
                    </div>
                    <div className="score-label">{getScoreBadge(rec.match_score)}</div>
                  </div>
                </div>

                {selectedCareer === index && (
                  <div className="career-details">
                    <div className="details-section">
                      <h4>💡 Why This Match?</h4>
                      <p>{rec.reasoning.summary}</p>
                      {rec.reasoning.strengths.length > 0 && (
                        <div>
                          <strong>Your Strengths:</strong>
                          <ul>
                            {rec.reasoning.strengths.map((strength, i) => (
                              <li key={i}>{strength}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>

                    <div className="details-section">
                      <h4>📚 Skills to Develop</h4>
                      {rec.skill_gaps.length > 0 ? (
                        <ul>
                          {rec.skill_gaps.map((skill, i) => (
                            <li key={i}>{skill}</li>
                          ))}
                        </ul>
                      ) : (
                        <p>You have all the fundamental skills!</p>
                      )}
                    </div>

                    <div className="details-section">
                      <h4>🚀 Learning Path</h4>
                      <ol>
                        {rec.learning_path.slice(0, 5).map((step, i) => (
                          <li key={i}>{step}</li>
                        ))}
                      </ol>
                    </div>

                    <div className="details-section">
                      <h4>📊 Career Stats</h4>
                      <div className="career-stats">
                        <div>
                          <strong>Market Demand:</strong>
                          <span>{rec.market_demand || 'N/A'}</span>
                        </div>
                        <div>
                          <strong>Growth Potential:</strong>
                          <span>{rec.growth_potential || 'N/A'}</span>
                        </div>
                        {rec.reasoning.market_potential && (
                          <div>
                            <strong>Future Outlook:</strong>
                            <span>{rec.reasoning.market_potential}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>No recommendations yet.</p>
            <p>Log some daily journal entries to help the AI understand your interests and generate personalized recommendations!</p>
          </div>
        )}

        <div className="tips-section">
          <h4>💫 How to Get Better Recommendations:</h4>
          <ul>
            <li>Complete your profile with honest information</li>
            <li>Log daily journal entries with your activities and learnings</li>
            <li>Share your challenges and growth areas</li>
            <li>Explore diverse interests and skills</li>
            <li>Update your profile as you grow</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default RecommendationsPage;
