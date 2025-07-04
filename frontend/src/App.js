import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import './App.css';
import { FaPaw, FaRandom, FaPlus, FaSyncAlt, FaSignOutAlt } from 'react-icons/fa';
import CatCareChatBubble from './pages/CatCareChatBubble';
import Login from './pages/Login';
import { TABS, API_BASE_URL, SUCCESS_MESSAGES, ERROR_MESSAGES } from './utils/constants';

function App() {
  // State management
  const [facts, setFacts] = useState([]);
  const [randomFact, setRandomFact] = useState(null);
  const [newFact, setNewFact] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [activeTab, setActiveTab] = useState(TABS.ALL);
  const [cursorPosition, setCursorPosition] = useState({ x: 0, y: 0 });
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState('');

  // Utility functions
  const showMessage = (text, isError = false) => {
    setMessage(text);
    if (!isError) {
      setTimeout(() => setMessage(''), 5000);
    }
  };

  const clearMessage = () => setMessage('');

  // API functions
  const fetchAllFacts = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/catfacts`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      // Handle new API response structure
      if (data.facts && Array.isArray(data.facts)) {
        setFacts(data.facts);
        showMessage(SUCCESS_MESSAGES.FACTS_LOADED);
      } else if (Array.isArray(data)) {
        // Fallback for old API structure
        setFacts(data);
        showMessage(SUCCESS_MESSAGES.FACTS_LOADED);
      } else {
        setFacts([]);
        throw new Error('Invalid response format from server');
      }
    } catch (error) {
      console.error('Fetch facts error:', error);
      const errorMessage = error.message.includes('Failed to fetch') 
        ? ERROR_MESSAGES.NETWORK_ERROR 
        : ERROR_MESSAGES.FETCH_FACTS_ERROR;
      showMessage(errorMessage, true);
      setFacts([]);
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchRandomFact = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/catfacts/random`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      setRandomFact(data);
      showMessage(SUCCESS_MESSAGES.RANDOM_FACT_LOADED);
    } catch (error) {
      console.error('Fetch random fact error:', error);
      const errorMessage = error.message.includes('Failed to fetch') 
        ? ERROR_MESSAGES.NETWORK_ERROR 
        : ERROR_MESSAGES.RANDOM_FACT_ERROR;
      showMessage(errorMessage, true);
      setRandomFact(null);
    } finally {
      setLoading(false);
    }
  };

  const addFact = async (e) => {
    e.preventDefault();
    if (!newFact.trim()) return;

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('fact', newFact.trim());

      const response = await fetch(`${API_BASE_URL}/catfacts`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      
      if (response.ok && (data.status === 'success' || data.success)) {
        showMessage(data.message || SUCCESS_MESSAGES.FACT_ADDED);
        setNewFact('');
        await fetchAllFacts(); // Refresh the facts list
      } else {
        throw new Error(data.detail || data.message || ERROR_MESSAGES.ADD_FACT_ERROR);
      }
    } catch (error) {
      console.error('Add fact error:', error);
      const errorMessage = error.message.includes('Failed to fetch') 
        ? ERROR_MESSAGES.NETWORK_ERROR 
        : error.message;
      showMessage(errorMessage, true);
    } finally {
      setLoading(false);
    }
  };

  // Authentication functions
  const handleLogin = () => {
    setIsAuthenticated(true);
    setUsername(localStorage.getItem('username'));
    showMessage('Welcome back!');
  };

  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('username');
    setIsAuthenticated(false);
    setUsername('');
    setFacts([]);
    setRandomFact(null);
    setActiveTab(TABS.ALL);
    showMessage('Logged out successfully!');
  };

  // Event handlers
  const handleTabChange = (tab) => {
    setActiveTab(tab);
    if (tab === TABS.RANDOM && !randomFact) {
      fetchRandomFact();
    }
  };

  const handleRefreshFacts = () => {
    fetchAllFacts();
  };

  // Effects
  useEffect(() => {
    // Check authentication status on component mount
    const authStatus = localStorage.getItem('isAuthenticated');
    const storedUsername = localStorage.getItem('username');
    
    if (authStatus === 'true' && storedUsername) {
      setIsAuthenticated(true);
      setUsername(storedUsername);
    }
  }, []);

  useEffect(() => {
    // Mouse cursor tracking
    const mouseMove = (e) => {
      setCursorPosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener("mousemove", mouseMove);
    
    return () => {
      window.removeEventListener("mousemove", mouseMove);
    };
  }, []);

  useEffect(() => {
    // Load facts when authenticated
    if (isAuthenticated) {
      fetchAllFacts();
    }
  }, [isAuthenticated, fetchAllFacts]);

  // Animation variants
  const cursorVariants = {
    default: {
      x: cursorPosition.x - 25,
      y: cursorPosition.y - 25,
    },
  };

  // Show login page if not authenticated
  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="App">
      <motion.div className="cursor" variants={cursorVariants} animate="default"/>
      
      <header className="App-header">
        <h1>
          <img 
            src="cat-angel.svg" 
            alt="Cat Angel" 
            style={{ 
              width: '100px', 
              height: '130px', 
              marginRight: '5px', 
              verticalAlign: 'middle',
              filter: 'drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.2))'
            }} 
          />
          Meowlogy - Cat Facts
        </h1>
        <h3>Welcome, {username}!</h3>
        <p>Discover amazing facts about our feline friends!</p>
      </header>

      <main className="App-main">
        {/* Navigation Tabs */}
        <div className="tabs">
          <button 
            className={`tab ${activeTab === TABS.ALL ? 'active' : ''}`}
            onClick={() => handleTabChange(TABS.ALL)}
          >
            <FaPaw className="tab-icon" />
            All Facts
          </button>
          <button 
            className={`tab ${activeTab === TABS.RANDOM ? 'active' : ''}`}
            onClick={() => handleTabChange(TABS.RANDOM)}
          >
            <FaRandom className="tab-icon" />
            Random Fact
          </button>
          <button 
            className={`tab ${activeTab === TABS.ADD ? 'active' : ''}`}
            onClick={() => handleTabChange(TABS.ADD)}
          >
            <FaPlus className="tab-icon" />
            Add Fact
          </button>
          <button 
            className={`tab ${activeTab === TABS.LOGOUT ? 'active' : ''}`}
            onClick={handleLogout} 
          >
            <FaSignOutAlt className="tab-icon" />
            Logout
          </button>
          <img 
            src="/holdingcat.svg" 
            className="cat-icon" 
            alt="Cute cat icon"
          />
        </div>

        {/* Message Display */}
        {message && (
          <div className={`message ${message.includes('Error') || message.includes('Failed') ? 'error' : 'success'}`}>
            {message}
            <button onClick={clearMessage} className="close-btn">×</button>
          </div>
        )}

        {/* Loading Indicator */}
        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Loading...</p>
          </div>
        )}

        {/* All Facts Tab */}
        {activeTab === TABS.ALL && (
          <div className="facts-container">
            <div className="section-header">
              <h2>All Cat Facts</h2>
              <button onClick={handleRefreshFacts} className="refresh-btn">
                <FaSyncAlt className="refresh-icon" />
                Refresh
              </button>
            </div>
            <div className="facts-grid">
              {facts.map((fact, index) => (
                <div key={index} className="fact-card">
                  <p>{fact.fact}</p>
                  <div className="fact-paw"></div>
                </div>
              ))}
            </div>
            {facts.length === 0 && !loading && (
              <p className="no-facts">No facts available. Add some facts to get started!</p>
            )}
          </div>
        )}

        {/* Random Fact Tab */}
        {activeTab === TABS.RANDOM && (
          <div className="random-fact-container">
            <h2>Random Cat Fact</h2>
            <button onClick={fetchRandomFact} className="random-btn">
              🎲 Get Random Fact
            </button>
            {randomFact && (
              <div className="random-fact-card">
                <p>{randomFact.fact}</p>
              </div>
            )}
          </div>
        )}

        {/* Add Fact Tab */}
        {activeTab === TABS.ADD && (
          <div className="add-fact-container">
            <h2>Add New Cat Fact</h2>
            <form onSubmit={addFact} className="add-fact-form">
              <textarea
                value={newFact}
                onChange={(e) => setNewFact(e.target.value)}
                placeholder="Enter your cat fact here..."
                rows="4"
                required
                disabled={loading}
              />
              <button type="submit" disabled={loading || !newFact.trim()}>
                {loading ? 'Adding...' : 'Add Fact'}
                <FaPaw className="paw-icon" />
              </button>
            </form>
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>Powered by FastAPI & React 🚀</p>
        <div className="footer-paws">
          <FaPaw />
          <FaPaw />
          <FaPaw />
        </div>
      </footer>

      <CatCareChatBubble />
    </div>
  );
}

export default App;
