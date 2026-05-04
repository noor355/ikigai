import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import robotImage from '../assets/illustrations/robot.png';
import './ChatPage.css';

function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input, timestamp: new Date().toISOString() };
    setMessages([...messages, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        'http://localhost:8000/api/v1/chat/',
        { message: input },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      const botMessage = { 
        role: 'assistant', 
        content: response.data.reply, 
        timestamp: new Date().toISOString() 
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again later.', 
        timestamp: new Date().toISOString() 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-page">
      <div className="chat-container">
        {/* Header with Illustration Space */}
        <div className="chat-header">
          <div className="chat-header-content">
            <div className="chat-header-text">
              <h2>🤖 AI Career Coach</h2>
              <p className="chat-subtitle">
                Chat with your AI mentor to get personalized career guidance based on your Ikigai profile!
              </p>
            </div>
            
            {/* Illustration Space */}
            <div className="chat-illustration-space">
              <div className="illustration-placeholder">
                <img 
                  src={robotImage}
                  alt="Robot illustration"
                  style={{ maxWidth: '100%', height: 'auto' }}
                />
              </div>
            </div>
          </div>
        </div>
      
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="chat-welcome">
            <p>👋 Hello! I'm your Ikigai Career Coach.</p>
            <p>Ask me anything about your career path!</p>
          </div>
        )}
        
        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-message chat-message-${msg.role}`}>
            <div className="chat-message-content">
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="chat-message chat-message-assistant">
            <div className="chat-message-content chat-thinking">
              Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSendMessage} className="chat-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          className="chat-input"
        />
        <button 
          type="submit" 
          disabled={loading}
          className="chat-send-button"
        >
          Send
        </button>
      </form>
      </div>
    </div>
  );
}

export default ChatPage;