import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaPaw, FaEye, FaEyeSlash } from 'react-icons/fa';
import './Login.css';
import { VALIDATION_RULES, ERROR_MESSAGES, API_BASE_URL } from '../utils/constants';

function Signup({ onSignupSuccess, onBackToLogin }) {
  // State management
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
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

  const validateEmail = (email) => {
    if (!email || typeof email !== 'string') {
      return ERROR_MESSAGES.EMAIL_REQUIRED;
    }

    const trimmedEmail = email.trim().toLowerCase();
    
    if (!VALIDATION_RULES.EMAIL.PATTERN.test(trimmedEmail)) {
      return ERROR_MESSAGES.EMAIL_INVALID;
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

  const validateConfirmPassword = (confirmPassword) => {
    if (!confirmPassword) {
      return 'Please confirm your password';
    }

    if (confirmPassword !== formData.password) {
      return 'Passwords do not match';
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

    // Validate email
    const emailError = validateEmail(formData.email);
    if (emailError) {
      newErrors.email = emailError;
    }

    // Validate password
    const passwordError = validatePassword(formData.password);
    if (passwordError) {
      newErrors.password = passwordError;
    }

    // Validate confirm password
    const confirmPasswordError = validateConfirmPassword(formData.confirmPassword);
    if (confirmPasswordError) {
      newErrors.confirmPassword = confirmPasswordError;
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
      const response = await fetch(`${API_BASE_URL}/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username.trim(),
          email: formData.email.trim().toLowerCase(),
          password: formData.password
        })
      });

      const data = await response.json();

      if (response.ok && data.success) {
        // Store authentication state
        localStorage.setItem('isAuthenticated', 'true');
        localStorage.setItem('username', data.user.username);
        localStorage.setItem('userId', data.user.id);
        
        onSignupSuccess();
      } else {
        // Handle specific error cases
        if (data.detail === 'Username already exists') {
          setErrors({ username: ERROR_MESSAGES.USERNAME_EXISTS });
        } else if (data.detail === 'Email already exists') {
          setErrors({ email: ERROR_MESSAGES.EMAIL_EXISTS });
        } else {
          setErrors({ general: data.detail || ERROR_MESSAGES.SIGNUP_FAILED });
        }
      }
    } catch (error) {
      console.error('Signup error:', error);
      setErrors({ general: ERROR_MESSAGES.SIGNUP_FAILED });
    } finally {
      setLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const toggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(!showConfirmPassword);
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
          <h1>Join Meowlogy</h1>
          <p>Create your account to access cat facts</p>
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
            <label htmlFor="email">Email</label>
            <div className="input-container">
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="Enter email"
                required
                className={`login-input ${errors.email ? 'error' : ''}`}
                disabled={loading}
              />
              <FaPaw className="input-icon" />
            </div>
            {errors.email && (
              <span className="field-error">{errors.email}</span>
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

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <div className="input-container">
              <input
                type={showConfirmPassword ? 'text' : 'password'}
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                placeholder="Confirm password"
                required
                className={`login-input ${errors.confirmPassword ? 'error' : ''}`}
                disabled={loading}
              />
              <button
                type="button"
                className="password-toggle"
                onClick={toggleConfirmPasswordVisibility}
                disabled={loading}
              >
                {showConfirmPassword ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>
            {errors.confirmPassword && (
              <span className="field-error">{errors.confirmPassword}</span>
            )}
          </div>

          <button 
            type="submit" 
            className="login-button"
            disabled={loading || !formData.username || !formData.email || !formData.password || !formData.confirmPassword}
          >
            {loading ? (
              <div className="loading-spinner">
                <div className="spinner"></div>
                Creating account...
              </div>
            ) : (
              <>
                <FaPaw className="paw-icon" />
                Sign Up
              </>
            )}
          </button>
        </form>

        <div className="login-hint">
          <p>Already have an account? <button onClick={onBackToLogin} className="link-button">Login here</button></p>
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

export default Signup; 