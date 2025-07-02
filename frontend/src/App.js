import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import './App.css';
import { FaPaw, FaRandom, FaPlus, FaSyncAlt } from 'react-icons/fa';
import CatCareChatBubble from './CatCareChatBubble';


function App() {
  const [facts, setFacts] = useState([]);
  const [randomFact, setRandomFact] = useState(null);
  const [newFact, setNewFact] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [activeTab, setActiveTab] = useState('all');
  const [cursorPosition, setCursorPosition] = useState({ x: 0, y: 0 });

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Fetch all facts
  const fetchAllFacts = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/catfacts`);
      if (response.ok) {
        const data = await response.json();
        setFacts(data);
      } else {
        setMessage('Failed to fetch facts');
      }
    } catch (error) {
      setMessage('Error connecting to server');
    } finally {
      setLoading(false);
    }
  };

  // Fetch random fact
  const fetchRandomFact = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/catfacts/random`);
      if (response.ok) {
        const data = await response.json();
        setRandomFact(data);
      } else {
        setMessage('Failed to fetch random fact');
      }
    } catch (error) {
      setMessage('Error connecting to server');
    } finally {
      setLoading(false);
    }
  };

  // Add new fact
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
      
      if (response.ok) {
        setMessage(data.message);
        setNewFact('');
        if (data.status === 'success') {
          fetchAllFacts(); // Refresh the facts list
        }
      } else {
        setMessage(data.detail || 'Failed to add fact');
      }
    } catch (error) {
      setMessage('Error connecting to server');
    } finally {
      setLoading(false);
    }
  };

  // Load facts on component mount
  useEffect(() => {
    const mouseMove = (e) => {
      setCursorPosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener("mousemove", mouseMove);
    return () => {
      fetchAllFacts();
      window.removeEventListener("mousemove", mouseMove);
    };
    
  }, []);

  const cursorVariants = {
    default: {
      x: cursorPosition.x - 25,
      y: cursorPosition.y - 25,
    },
  };

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
        <p>Discover amazing facts about our feline friends!</p>
      </header>

      <main className="App-main">
        {/* Navigation Tabs */}
        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'all' ? 'active' : ''}`}
            onClick={() => setActiveTab('all')}
          >
            <FaPaw className="tab-icon" />
            All Facts
          </button>
          <button 
            className={`tab ${activeTab === 'random' ? 'active' : ''}`}
            onClick={() => setActiveTab('random')}
          >
            <FaRandom className="tab-icon" />
            Random Fact
          </button>
          <button 
            className={`tab ${activeTab === 'add' ? 'active' : ''}`}
            onClick={() => setActiveTab('add')}
          >
            <FaPlus className="tab-icon" />
            Add Fact
          </button>
          <img 
            src="http://thecraftchop.com/files/others/holdingcat.svg" 
            className="cat-icon" 
            alt="Cute cat icon"
          />
        </div>

        {/* Message Display */}
        {message && (
          <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
            {message}
            <button onClick={() => setMessage('')} className="close-btn">×</button>
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
        {activeTab === 'all' && (
          <div className="facts-container">
            <div className="section-header">
              <h2>All Cat Facts</h2>
              <button onClick={fetchAllFacts} className="refresh-btn">
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
        {activeTab === 'random' && (
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
        {activeTab === 'add' && (
          <div className="add-fact-container">
            <h2>Add New Cat Fact</h2>
            <form onSubmit={addFact} className="add-fact-form">
              <textarea
                value={newFact}
                onChange={(e) => setNewFact(e.target.value)}
                placeholder="Enter your cat fact here..."
                rows="4"
                required
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
