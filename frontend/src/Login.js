import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaPaw, FaEye, FaEyeSlash } from 'react-icons/fa';
import './Login.css';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [cursorPosition, setCursorPosition] = useState({ x: 0, y: 0 });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Simulate API call delay
    setTimeout(() => {
      if (username === 'JAY' && password === 'JAY') {
        // Store authentication state
        localStorage.setItem('isAuthenticated', 'true');
        localStorage.setItem('username', username);
        onLogin();
      } else {
        setError('Invalid username or password. Please use JAY for both fields.');
      }
      setLoading(false);
    }, 1000);
  };

  // Mouse cursor tracking
  useEffect(() => {
    const mouseMove = (e) => {
      setCursorPosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener("mousemove", mouseMove);
    return () => {
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
    <div className="login-container">
      <motion.div className="cursor" variants={cursorVariants} animate="default"/>
      <motion.div 
        className="login-card"
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="login-header">
          <img 
            src="cat-angel.svg" 
            alt="Cat Angel" 
            className="login-logo"
          />
          <h1>Welcome to Meowlogy</h1>
          <p>Please login to access cat facts</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="username">Username</label>
            <div className="input-container">
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter username"
                required
                className="login-input"
              />
              <FaPaw className="input-icon" />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <div className="input-container">
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
                required
                className="login-input"
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>
          </div>

          <button 
            type="submit" 
            className="login-button"
            disabled={loading || !username || !password}
          >
            {loading ? (
              <div className="loading-spinner">
                <div className="spinner"></div>
                Logging in...
              </div>
            ) : (
              <>
                <FaPaw className="paw-icon" />
                Login
              </>
            )}
          </button>
        </form>

        <div className="login-hint">
          <p>💡 Hint: Use "JAY" for both username and password</p>
        </div>

        <div className="login-footer">
          <div className="footer-paws">
            <FaPaw />
            <FaPaw />
            <FaPaw />
          </div>
        </div>
      </motion.div>
    </div>
  );
}

export default Login; 