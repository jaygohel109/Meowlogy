import React, { useState, useRef, useEffect } from 'react';
import './CatCareChatBubble.css';
import { FaPaw } from 'react-icons/fa';

const API_URL = 'http://localhost:8000/api/ask-ai'; // Update if backend URL changes

const CatCareChatBubble = () => {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { sender: 'ai', text: 'Hi! Ask me anything about cat care 🐾' }
  ]);
  const [loading, setLoading] = useState(false);
  const messageEndRef = useRef(null);

  useEffect(() => {
    if (open && messageEndRef.current) {
      messageEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [open, messages]);

  const handleSend = async () => {
    const question = input.trim();
    if (!question) return;
    setMessages(prev => [...prev, { sender: 'user', text: question }]);
    setInput('');
    setLoading(true);
  
    let aiMessage = '';
    setMessages(prev => [...prev, { sender: 'ai', text: '' }]);
  
    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
  
      if (!res.body) throw new Error('No response body');
  
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let done = false;
  
      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        if (value) {
          const chunk = decoder.decode(value);
          aiMessage += chunk;
          setMessages(prev => {
            // Update the last AI message with the new chunk
            const updated = [...prev];
            updated[updated.length - 1] = { sender: 'ai', text: aiMessage };
            return updated;
          });
        }
      }
    } catch (err) {
      setMessages(prev => [...prev, { sender: 'ai', text: 'Sorry, there was an error connecting to the AI.' }]);
    }
    setLoading(false);
  };

  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter' && !loading) {
      handleSend();
    }
  };

  return (
    <div className="catcare-chat-bubble-container">
      {open && (
        <div className="catcare-chat-window">
          <div className="catcare-chat-header">
            Cat Care AI
            <button className="catcare-chat-close" onClick={() => setOpen(false)}>&times;</button>
          </div>
          <div className="catcare-chat-messages">
            {loading && (
              <div className="catcare-chat-message catcare-chat-message-ai catcare-chat-loading">
                <span className="">
                  <div className="footer-paws">
                    <FaPaw />
                    <FaPaw />
                    <FaPaw />
                  </div>
                </span>
              </div>
            )}
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`catcare-chat-message catcare-chat-message-${msg.sender}`}
              >
                {msg.text}
              </div>
            ))}
            <div ref={messageEndRef} />
          </div>
          <div className="catcare-chat-input-row">
            <input
              className="catcare-chat-input"
              type="text"
              placeholder="Type your question..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleInputKeyDown}
              disabled={loading}
              autoFocus
            />
            <button
              className="catcare-chat-send"
              onClick={handleSend}
              disabled={loading || !input.trim()}
            >
              Send
            </button>
          </div>
        </div>
      )}
      <div className="catcare-chat-icon-wrapper">
        {!open && (
          <div className="catcare-speech-bubble" onClick={() => setOpen(true)}>
            ASK AI
          </div>
        )}
        <img
          src="/icons8-cat-head-48.png"
          alt="Cat Icon"
          className="catcare-chat-gif"
          onClick={() => setOpen(true)}
        />
      </div>
    </div>
  );
};

export default CatCareChatBubble; 