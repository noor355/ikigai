import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

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
    <div style={{ 
      padding: "30px 20px", 
      fontFamily: "'Inter', system-ui, sans-serif", 
      maxWidth: "900px", 
      margin: "0 auto",
      height: "calc(100vh - 120px)",
      display: "flex",
      flexDirection: "column",
      backgroundColor: "#fff",
      borderRadius: "16px",
      boxShadow: "0 4px 20px rgba(0,0,0,0.03)"
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: "25px", borderBottom: "1px solid #f0f4f8", paddingBottom: "15px" }}>
        <div style={{ backgroundColor: "#4299e1", color: "white", padding: "10px", borderRadius: "12px", display: "flex", alignItems: "center" }}>
          <span style={{ fontSize: "20px" }}>🤖</span>
        </div>
        <div>
          <h2 style={{ color: "#1a202c", margin: 0, fontSize: "20px" }}>AI Career Coach</h2>
          <span style={{ color: "#718096", fontSize: "13px" }}>Online | Helping you find your Ikigai</span>
        </div>
      </div>
      
      <div style={{ 
        flex: 1, 
        overflowY: "auto", 
        padding: "10px 5px", 
        marginBottom: "20px",
        scrollbarWidth: "none"
      }}>
        {messages.length === 0 && (
          <div style={{ textAlign: "center", color: "#718096", marginTop: "40px" }}>
            <p>👋 Hello! I'm your Ikigai Career Coach.</p>
            <p>Ask me anything about your career path!</p>
          </div>
        )}
        
        {messages.map((msg, idx) => (
          <div key={idx} style={{ 
            display: "flex", 
            justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
            marginBottom: "15px"
          }}>
            <div style={{ 
              maxWidth: "75%", 
              padding: "12px 18px", 
              borderRadius: msg.role === 'user' ? "18px 18px 2px 18px" : "18px 18px 18px 2px",
              backgroundColor: msg.role === 'user' ? '#4299e1' : '#ffffff',
              color: msg.role === 'user' ? 'white' : '#2d3748',
              boxShadow: "0 2px 4px rgba(0,0,0,0.05)",
              border: msg.role === 'user' ? "none" : "1px solid #e2e8f0",
              lineHeight: "1.5",
              fontSize: "15px",
              whiteSpace: "pre-wrap"
            }}>
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ display: "flex", justifyContent: "flex-start", marginBottom: "15px" }}>
            <div style={{ 
              backgroundColor: '#edf2f7', 
              padding: "12px 16px", 
              borderRadius: "18px",
              color: "#718096"
            }}>
              Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSendMessage} style={{ display: "flex", gap: "10px" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          style={{ 
            flex: 1, 
            padding: "12px 20px", 
            borderRadius: "25px", 
            border: "1px solid #cbd5e0",
            outline: "none",
            fontSize: "16px"
          }}
        />
        <button 
          type="submit" 
          disabled={loading}
          style={{ 
            padding: "12px 24px", 
            borderRadius: "25px", 
            backgroundColor: "#4299e1", 
            color: "white", 
            border: "none",
            cursor: "pointer",
            fontWeight: "bold",
            transition: "background-color 0.2s"
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
}

export default ChatPage;