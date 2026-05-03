import React, { useState } from 'react';
import axios from 'axios';
import { FiEdit3, FiBookOpen, FiAlertCircle, FiSmile, FiSave, FiZap } from 'react-icons/fi';
import { MdAutoAwesome } from 'react-icons/md';
import './JournalPage.css';

const JournalPage = () => {
  const [formData, setFormData] = useState({
    activities: [],
    learnings: '',
    challenges: '',
    mood: 'neutral',
    notes: '',
    currentActivity: '',
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleActivityAdd = () => {
    if (formData.currentActivity.trim()) {
      setFormData({
        ...formData,
        activities: [...formData.activities, formData.currentActivity.trim()],
        currentActivity: '',
      });
    }
  };

  const handleActivityRemove = (index) => {
    setFormData({
      ...formData,
      activities: formData.activities.filter((_, i) => i !== index),
    });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const token = localStorage.getItem('token');
      
      const response = await axios.post(
        'http://localhost:8000/api/v1/recommendations/save-daily-entry',
        {
          activities: formData.activities.length > 0 ? formData.activities : ['Journal entry'],
          learnings: formData.learnings || null,
          challenges: formData.challenges || null,
          mood: formData.mood,
          notes: formData.notes || null,
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );

      setMessage('✅ Daily entry saved! This helps personalize your career recommendations.');
      
      // Reset form
      setFormData({
        activities: [],
        learnings: '',
        challenges: '',
        mood: 'neutral',
        notes: '',
        currentActivity: '',
      });
    } catch (error) {
      console.error("Submission error", error);
      if (error.response && error.response.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "/";
      }
      setMessage(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="journal-page">
      <div className="journal-container">
        {/* Header with Illustration Space */}
        <div className="journal-header">
          <div className="journal-header-content">
            <div className="journal-header-text">
              <h2><FiEdit3 style={{ display: 'inline', marginRight: '10px' }} />Daily Journal</h2>
              <p className="journal-subtitle">
                Record your daily activities, learnings, and experiences. The AI analyzes these to recommend the perfect career for you!
              </p>
            </div>
            
            {/* Illustration Space */}
            <div className="journal-illustration-space">
              <div className="illustration-placeholder">
                <img 
                  src="/illustrations/journal-meditation.svg"
                  alt="Journal illustration"
                  style={{ maxWidth: '100%', height: 'auto' }}
                />
              </div>
            </div>
          </div>
        </div>

      {message && (
        <div className={`message ${message.includes('✅') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="journal-form">
        {/* Helper Prompts */}
        <div className="helper-prompts">
          <small style={{ fontWeight: 'bold', color: 'var(--text-200)', display: 'block', marginBottom: '8px' }}>
            <MdAutoAwesome style={{ display: 'inline', marginRight: '6px', fontSize: '16px' }} />
            Need inspiration? Try writing about:
          </small>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {['Working with data', 'Designing apps', 'Leading a team', 'Problem solving', 'Cybersecurity'].map(prompt => (
              <button 
                type="button"
                key={prompt}
                onClick={() => setFormData({...formData, currentActivity: prompt})}
                className="prompt-button"
              >
                + {prompt}
              </button>
            ))}
          </div>
        </div>

        {/* Activities */}
        <div className="form-section">
          <label className="form-label">
            <FiZap style={{ display: 'inline', marginRight: '8px' }} />
            What did you do today?
          </label>
          <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
            <input
              type="text"
              placeholder="E.g., Coded, Analyzed data, Designed UI..."
              value={formData.currentActivity}
              onChange={(e) => setFormData({ ...formData, currentActivity: e.target.value })}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleActivityAdd();
                }
              }}
              className="activity-input"
            />
            <button
              type="button"
              onClick={handleActivityAdd}
              className="btn-add"
            >
              + Add
            </button>
          </div>

          <div className="activities-list">
            {formData.activities.map((activity, index) => (
              <div key={index} className="activity-tag">
                <span>{activity}</span>
                <button
                  type="button"
                  onClick={() => handleActivityRemove(index)}
                  className="btn-remove"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Learnings */}
        <div className="form-section">
          <label className="form-label">
            <FiBookOpen style={{ display: 'inline', marginRight: '8px' }} />
            What did you learn?
          </label>
          <textarea
            name="learnings"
            placeholder="New skills, insights, concepts..."
            value={formData.learnings}
            onChange={handleInputChange}
            rows="3"
            className="form-textarea"
          />
        </div>

        {/* Challenges */}
        <div className="form-section">
          <label className="form-label">
            <FiAlertCircle style={{ display: 'inline', marginRight: '8px' }} />
            What was challenging?
          </label>
          <textarea
            name="challenges"
            placeholder="Difficulties, what made you think, areas to improve..."
            value={formData.challenges}
            onChange={handleInputChange}
            rows="3"
            className="form-textarea"
          />
        </div>

        {/* Mood */}
        <div className="form-section">
          <label className="form-label">
            <FiSmile style={{ display: 'inline', marginRight: '8px' }} />
            How was your mood?
          </label>
          <div className="mood-options">
            {[
              { value: 'very_happy', emoji: '😄', label: 'Very Happy' },
              { value: 'happy', emoji: '😊', label: 'Happy' },
              { value: 'neutral', emoji: '😐', label: 'Neutral' },
              { value: 'sad', emoji: '😔', label: 'Sad' },
              { value: 'very_sad', emoji: '😢', label: 'Very Sad' },
            ].map((mood) => (
              <label key={mood.value} className="mood-option">
                <input
                  type="radio"
                  name="mood"
                  value={mood.value}
                  checked={formData.mood === mood.value}
                  onChange={handleInputChange}
                />
                <span className="mood-emoji">{mood.emoji}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Notes */}
        <div className="form-section">
          <label className="form-label">
            📌 Notes
          </label>
          <textarea
            name="notes"
            placeholder="Any other thoughts or observations..."
            value={formData.notes}
            onChange={handleInputChange}
            rows="3"
            className="form-textarea"
          />
        </div>

        <button type="submit" disabled={loading} className="btn-submit">
          <FiSave style={{ display: 'inline', marginRight: '8px' }} />
          {loading ? 'Saving...' : 'Save Entry & Update Recommendations'}
        </button>
      </form>

      <div className="journal-tips">
        <h4>💫 Tips for Better Recommendations:</h4>
        <ul>
          <li><strong>Be honest:</strong> Record what you actually did</li>
          <li><strong>Be specific:</strong> Details help the AI understand you</li>
          <li><strong>Be consistent:</strong> Daily entries improve accuracy</li>
          <li><strong>Share challenges:</strong> Growth areas define your ideal career</li>
        </ul>
      </div>
      </div>
    </div>
  );
};

export default JournalPage;