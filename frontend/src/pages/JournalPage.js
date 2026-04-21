import React, { useState } from 'react';
import axios from 'axios';
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
    <div style={{ padding: '40px', fontFamily: 'sans-serif', maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ marginBottom: '30px' }}>
        <h2 style={{ margin: '0 0 10px 0' }}>📝 Daily Journal</h2>
        <p style={{ color: '#6c757d', margin: 0 }}>
          Record your daily activities, learnings, and experiences. The AI analyzes these to recommend the perfect career for you!
        </p>
      </div>

      {message && (
        <div style={{
          padding: '12px 16px',
          marginBottom: '20px',
          borderRadius: '4px',
          backgroundColor: message.includes('✅') ? '#d4edda' : '#f8d7da',
          color: message.includes('✅') ? '#155724' : '#721c24',
          border: `1px solid ${message.includes('✅') ? '#c3e6cb' : '#f5c6cb'}`,
        }}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ backgroundColor: '#f8f9fa', padding: '24px', borderRadius: '8px' }}>
        {/* Helper Prompts */}
        <div style={{ marginBottom: '20px', padding: '12px', background: '#e9ecef', borderRadius: '6px' }}>
          <small style={{ fontWeight: 'bold', color: '#495057', display: 'block', marginBottom: '5px' }}>💡 Need inspiration? Try writing about:</small>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
            {['Working with data', 'Designing apps', 'Leading a team', 'Problem solving', 'Cybersecurity'].map(prompt => (
              <button 
                type="button"
                key={prompt}
                onClick={() => setFormData({...formData, currentActivity: prompt})}
                style={{ fontSize: '11px', padding: '2px 8px', borderRadius: '15px', border: '1px solid #ced4da', cursor: 'pointer', background: 'white' }}
              >
                + {prompt}
              </button>
            ))}
          </div>
        </div>

        {/* Activities */}
        <div style={{ marginBottom: '24px' }}>
          <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '8px' }}>🎯 What did you do today?</label>
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
              style={{
                flex: 1,
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '14px',
              }}
            />
            <button
              type="button"
              onClick={handleActivityAdd}
              style={{
                padding: '10px 16px',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              + Add
            </button>
          </div>

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {formData.activities.map((activity, index) => (
              <div
                key={index}
                style={{
                  backgroundColor: '#e2e3e5',
                  padding: '6px 12px',
                  borderRadius: '20px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  fontSize: '14px',
                }}
              >
                <span>{activity}</span>
                <button
                  type="button"
                  onClick={() => handleActivityRemove(index)}
                  style={{
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    color: '#999',
                  }}
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Learnings */}
        <div style={{ marginBottom: '24px' }}>
          <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '8px' }}>💡 What did you learn?</label>
          <textarea
            name="learnings"
            placeholder="New skills, insights, concepts..."
            value={formData.learnings}
            onChange={handleInputChange}
            rows="3"
            style={{
              width: '100%',
              padding: '10px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              fontFamily: 'inherit',
              fontSize: '14px',
              boxSizing: 'border-box',
            }}
          />
        </div>

        {/* Challenges */}
        <div style={{ marginBottom: '24px' }}>
          <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '8px' }}>⚡ What was challenging?</label>
          <textarea
            name="challenges"
            placeholder="Difficulties, what made you think, areas to improve..."
            value={formData.challenges}
            onChange={handleInputChange}
            rows="3"
            style={{
              width: '100%',
              padding: '10px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              fontFamily: 'inherit',
              fontSize: '14px',
              boxSizing: 'border-box',
            }}
          />
        </div>

        {/* Mood */}
        <div style={{ marginBottom: '24px' }}>
          <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '12px' }}>😊 How was your mood?</label>
          <div style={{ display: 'flex', gap: '16px' }}>
            {[
              { value: 'very_happy', emoji: '😄', label: 'Very Happy' },
              { value: 'happy', emoji: '😊', label: 'Happy' },
              { value: 'neutral', emoji: '😐', label: 'Neutral' },
              { value: 'sad', emoji: '😔', label: 'Sad' },
              { value: 'very_sad', emoji: '😢', label: 'Very Sad' },
            ].map((mood) => (
              <label key={mood.value} style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                <input
                  type="radio"
                  name="mood"
                  value={mood.value}
                  checked={formData.mood === mood.value}
                  onChange={handleInputChange}
                />
                <span style={{ fontSize: '20px' }}>{mood.emoji}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Notes */}
        <div style={{ marginBottom: '24px' }}>
          <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '8px' }}>📌 Notes</label>
          <textarea
            name="notes"
            placeholder="Any other thoughts or observations..."
            value={formData.notes}
            onChange={handleInputChange}
            rows="3"
            style={{
              width: '100%',
              padding: '10px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              fontFamily: 'inherit',
              fontSize: '14px',
              boxSizing: 'border-box',
            }}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{
            width: '100%',
            padding: '12px',
            backgroundColor: loading ? '#ccc' : '#28a745',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            fontSize: '16px',
            fontWeight: 'bold',
            cursor: loading ? 'default' : 'pointer',
          }}
        >
          {loading ? '⏳ Saving...' : '💾 Save Entry & Update Recommendations'}
        </button>
      </form>

      <div style={{
        marginTop: '32px',
        padding: '20px',
        backgroundColor: '#e7f3ff',
        borderRadius: '8px',
        border: '1px solid #b3d9ff',
      }}>
        <h4 style={{ marginTop: 0 }}>💫 Tips for Better Recommendations:</h4>
        <ul style={{ margin: '10px 0', paddingLeft: '20px' }}>
          <li><strong>Be honest:</strong> Record what you actually did</li>
          <li><strong>Be specific:</strong> Details help the AI understand you</li>
          <li><strong>Be consistent:</strong> Daily entries improve accuracy</li>
          <li><strong>Share challenges:</strong> Growth areas define your ideal career</li>
        </ul>
      </div>
    </div>
  );
};

export default JournalPage;