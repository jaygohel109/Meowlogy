import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaPaw, FaEye, FaEyeSlash } from 'react-icons/fa';
import './Login.css';
import { VALIDATION_RULES, ERROR_MESSAGES, DEMO_CREDENTIALS } from '../utils/constants';

function Login({ onLogin }) {
  // State management
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [cursorPosition, setCursorPosition] = useState({ x: 0, y: 0 });

  // Utility functions
  const validateUsername = (username) => {
    if (!username || typeof username !== 'string') {
      return ERROR_MESSAGES.USERNAME_REQUIRED;
    }

    const trimmedUsername = username.trim();
    
    if (trimmedUsername.length < VALIDATION_RULES.USERNAME.MIN_LENGTH) {
      return ERROR_MESSAGES.USERNAME_TOO_SHORT;
    }

    if (trimmedUsername.length > VALIDATION_RULES.USERNAME.MAX_LENGTH) {
      return ERROR_MESSAGES.USERNAME_TOO_LONG;
    }

    if (!VALIDATION_RULES.USERNAME.PATTERN.test(trimmedUsername)) {
      return ERROR_MESSAGES.USERNAME_INVALID;
    }

    return null;
  };

  const validatePassword = (password) => {
    if (!password || typeof password !== 'string') {
      return ERROR_MESSAGES.PASSWORD_REQUIRED;
    }

    if (password.length < VALIDATION_RULES.PASSWORD.MIN_LENGTH) {
      return ERROR_MESSAGES.PASSWORD_TOO_SHORT;
    }

    return null;
  };

  const validateForm = () => {
    const newErrors = {};

    // Validate username
    const usernameError = validateUsername(formData.username);
    if (usernameError) {
      newErrors.username = usernameError;
    }

    // Validate password
    const passwordError = validatePassword(formData.password);
    if (passwordError) {
      newErrors.password = passwordError;
    }

    // Check credentials
    if (formData.username !== DEMO_CREDENTIALS.USERNAME || 
        formData.password !== DEMO_CREDENTIALS.PASSWORD) {
      newErrors.general = ERROR_MESSAGES.INVALID_CREDENTIALS;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const clearFieldError = (fieldName) => {
    if (errors[fieldName]) {
      setErrors(prev => ({
        ...prev,
        [fieldName]: ''
      }));
    }
  };

  // Event handlers
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear field error when user starts typing
    clearFieldError(name);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Store authentication state
      localStorage.setItem('isAuthenticated', 'true');
      localStorage.setItem('username', formData.username.trim());
      
      onLogin();
    } catch (error) {
      console.error('Login error:', error);
      setErrors({ general: ERROR_MESSAGES.LOGIN_FAILED });
    } finally {
      setLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  // Effects
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

  // Animation variants
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
          {errors.general && (
            <div className="error-message">
              {errors.general}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="username">Username</label>
            <div className="input-container">
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleInputChange}
                placeholder="Enter username"
                required
                className={`login-input ${errors.username ? 'error' : ''}`}
                disabled={loading}
              />
              <FaPaw className="input-icon" />
            </div>
            {errors.username && (
              <span className="field-error">{errors.username}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <div className="input-container">
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                placeholder="Enter password"
                required
                className={`login-input ${errors.password ? 'error' : ''}`}
                disabled={loading}
              />
              <button
                type="button"
                className="password-toggle"
                onClick={togglePasswordVisibility}
                disabled={loading}
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>
            {errors.password && (
              <span className="field-error">{errors.password}</span>
            )}
          </div>

          <button 
            type="submit" 
            className="login-button"
            disabled={loading || !formData.username || !formData.password}
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