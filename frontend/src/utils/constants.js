// Constants
// Validation rules
const VALIDATION_RULES = {
  QUESTION: {
        MIN_LENGTH: 5,
        MAX_LENGTH: 500
  },
  USERNAME: {
    MIN_LENGTH: 2,
    MAX_LENGTH: 50,
    PATTERN: /^[a-zA-Z0-9_\s]+$/
  },
  PASSWORD: {
    MIN_LENGTH: 6
  },
  EMAIL: {
    PATTERN: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  }
};

// Error messages
const ERROR_MESSAGES = {
    QUESTION_TOO_SHORT: `Question must be at least ${VALIDATION_RULES.QUESTION.MIN_LENGTH} characters long`,
    QUESTION_TOO_LONG: `Question must be no more than ${VALIDATION_RULES.QUESTION.MAX_LENGTH} characters long`,
    NETWORK_ERROR: 'Network error. Please check your connection.',
    AI_SERVICE_ERROR: 'Sorry, there was an error connecting to the AI service.',
    NO_RESPONSE: 'No response received from AI service.',
    USERNAME_REQUIRED: 'Username is required',
    USERNAME_TOO_SHORT: `Username must be at least ${VALIDATION_RULES.USERNAME.MIN_LENGTH} characters long`,
    USERNAME_TOO_LONG: `Username must be no more than ${VALIDATION_RULES.USERNAME.MAX_LENGTH} characters long`,
    USERNAME_INVALID: 'Username can only contain letters, numbers, spaces, and underscores',
    PASSWORD_REQUIRED: 'Password is required',
    PASSWORD_TOO_SHORT: `Password must be at least ${VALIDATION_RULES.PASSWORD.MIN_LENGTH} characters long`,
    EMAIL_REQUIRED: 'Email is required',
    EMAIL_INVALID: 'Please enter a valid email address',
    INVALID_CREDENTIALS: 'Invalid username or password.',
    LOGIN_FAILED: 'Login failed. Please try again.',
    SIGNUP_FAILED: 'Signup failed. Please try again.',
    USERNAME_EXISTS: 'Username already exists.',
    EMAIL_EXISTS: 'Email already exists.',
    SERVER_ERROR: 'Server error. Please try again later.',
    FETCH_FACTS_ERROR: 'Failed to fetch cat facts.',
    ADD_FACT_ERROR: 'Failed to add fact. Please try again.',
    RANDOM_FACT_ERROR: 'Failed to fetch random fact.',
    UNKNOWN_ERROR: 'An unexpected error occurred.'
};

// Initial welcome message
const WELCOME_MESSAGE = {
  sender: 'ai',
  text: 'Hi! I\'m your Cat Care Buddy — Ask me anything about your feline friend! 🐾',
  timestamp: new Date()
};


// Constants
const DEMO_CREDENTIALS = {
    USERNAME: 'JAY',
    PASSWORD: 'JAY'
  };
  

  // Constants
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const TABS = {
  ALL: 'all',
  RANDOM: 'random',
  ADD: 'add',
  LOGOUT: 'logout'
};

// Success messages
const SUCCESS_MESSAGES = {
  FACT_ADDED: 'Cat fact added successfully!',
  FACTS_LOADED: 'Cat facts loaded successfully!',
  RANDOM_FACT_LOADED: 'Random fact loaded!'
};

export { VALIDATION_RULES, ERROR_MESSAGES, WELCOME_MESSAGE, DEMO_CREDENTIALS, API_BASE_URL, TABS, SUCCESS_MESSAGES };