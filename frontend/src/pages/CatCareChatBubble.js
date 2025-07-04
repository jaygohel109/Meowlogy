import React, { useState, useRef, useEffect } from 'react';
import './CatCareChatBubble.css';
import { WELCOME_MESSAGE, VALIDATION_RULES, API_BASE_URL, ERROR_MESSAGES } from '../utils/constants';


const CatCareChatBubble = () => {
  // State management
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const messageEndRef = useRef(null);

  // Utility functions
  const validateQuestion = (question) => {
    const trimmedQuestion = question.trim();
    
    if (trimmedQuestion.length < VALIDATION_RULES.QUESTION.MIN_LENGTH) {
      return ERROR_MESSAGES.QUESTION_TOO_SHORT;
    }

    if (trimmedQuestion.length > VALIDATION_RULES.QUESTION.MAX_LENGTH) {
      return ERROR_MESSAGES.QUESTION_TOO_LONG;
    }

    return null;
  };

  const addMessage = (sender, text) => {
    const newMessage = {
      sender,
      text,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const updateLastAIMessage = (text) => {
    setMessages(prev => {
      const updated = [...prev];
      if (updated.length > 0 && updated[updated.length - 1].sender === 'ai') {
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          text
        };
      }
      return updated;
    });
  };

  const clearError = () => {
    setError('');
  };

  const clearChat = () => {
    setMessages([WELCOME_MESSAGE]);
    clearError();
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Event handlers
  const handleSend = async () => {
    const question = input.trim();
    
    // Validate input
    const validationError = validateQuestion(question);
    if (validationError) {
      setError(validationError);
      return;
    }

    // Clear previous error
    clearError();

    // Add user message
    addMessage('user', question);
    setInput('');
    setLoading(true);

    // Add empty AI message placeholder
    addMessage('ai', '');

    try {
      let aiMessage = '';

      const response = await fetch(`${API_BASE_URL}/api/ask-ai`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      if (!response.body) {
        throw new Error(ERROR_MESSAGES.NO_RESPONSE);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      try {
        while (true) {
          const { done, value } = await reader.read();
          
          if (done) break;
          
          if (value) {
            const chunk = decoder.decode(value);
            aiMessage += chunk;
            updateLastAIMessage(aiMessage);
          }
        }
      } finally {
        reader.releaseLock();
      }

      // Final update to ensure complete message
      updateLastAIMessage(aiMessage);

    } catch (err) {
      console.error('AI Chat Error:', err);
      const errorMessage = err.message.includes('Failed to fetch') 
        ? ERROR_MESSAGES.NETWORK_ERROR 
        : ERROR_MESSAGES.AI_SERVICE_ERROR;
      updateLastAIMessage(`Sorry, there was an error: ${errorMessage}`);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !loading) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
    // Clear error when user starts typing
    if (error) {
      clearError();
    }
  };

  const toggleChat = () => {
    setOpen(!open);
    if (!open) {
      // Clear error when opening chat
      clearError();
    }
  };

  // Effects
  useEffect(() => {
    // Auto-scroll to bottom when new messages arrive
    if (open && messageEndRef.current) {
      messageEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [open, messages]);

  return (
    <div className="catcare-chat-bubble-container">
      {open && (
        <div className="catcare-chat-window">
          <div className="catcare-chat-header">
            <div className="catcare-chat-title">
              <span>🐱 Cat Care AI</span>
              <span className="catcare-chat-subtitle">Powered by AI</span>
            </div>
            <div className="catcare-chat-controls">
              <button 
                className="catcare-chat-clear" 
                onClick={clearChat}
                title="Clear chat"
              >
                🗑️
              </button>
              <button 
                className="catcare-chat-close" 
                onClick={toggleChat}
                title="Close chat"
              >
                &times;
              </button>
            </div>
          </div>

          <div className="catcare-chat-messages">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`catcare-chat-message catcare-chat-message-${msg.sender}`}
              >
                <div className="catcare-chat-message-content">
                  {msg.text}
                </div>
                <div className="catcare-chat-message-time">
                  {formatTime(msg.timestamp)}
                </div>
              </div>
            ))}
            {loading && (
              <div className="catcare-chat-message catcare-chat-message-ai">
                <div className="catcare-chat-message-content">
                  <div className="loading-dots">
                    <div className="dot"></div>
                    <div className="dot"></div>
                    <div className="dot"></div>
                  </div>
                  AI is thinking...
                </div>
              </div>
            )}
            <div ref={messageEndRef} />
          </div>

          {error && (
            <div className="catcare-chat-error">
              {error}
            </div>
          )}

          <div className="catcare-chat-input-row">
            <input
              className="catcare-chat-input"
              type="text"
              placeholder="Type your question about cats..."
              value={input}
              onChange={handleInputChange}
              onKeyDown={handleInputKeyDown}
              disabled={loading}
              autoFocus
            />
            <button
              className="catcare-chat-send"
              onClick={handleSend}
              disabled={loading || !input.trim()}
              title="Send message"
            >
              {loading ? '⏳' : '📤'}
            </button>
          </div>
        </div>
      )}

      <div className="catcare-chat-icon-wrapper">
        {!open && (
          <div className="catcare-speech-bubble" onClick={toggleChat}>
            Meowgic AI
          </div>
        )}
        <img
          src="/icons8-cat-head-48.png"
          alt="Cat Icon"
          className="catcare-chat-gif"
          onClick={toggleChat}
        />
      </div>
    </div>
  );
};

export default CatCareChatBubble; 