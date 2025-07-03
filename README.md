# Cat Facts API - Backend

A well-structured FastAPI backend for managing cat facts with Supabase integration and AI-powered cat care assistance.

## 🏗️ Architecture Overview

This backend follows a clean, senior-level architecture with proper separation of concerns:

```
Backend/
├── config.py              # Configuration management
├── constants.py           # Centralized constants and messages
├── exceptions.py          # Custom exception classes
├── main.py               # FastAPI application entry point
├── requirements.txt      # Python dependencies
├── supabase_db.py        # Database layer (Supabase)
├── import_cat_facts.py   # External API integration
├── Models/               # Data models and schemas
│   ├── __init__.py
│   ├── cat_facts_models.py
│   └── openAI_model.py
└── services/            # Business logic layer
    ├── __init__.py
    ├── cat_facts_service.py
    └── ai_service.py
```

## 🚀 Features

- **RESTful API** with comprehensive CRUD operations for cat facts
- **Supabase Integration** for scalable database operations
- **AI-Powered Chat** for cat care advice using OpenAI
- **Data Validation** with Pydantic models
- **Comprehensive Error Handling** with custom exceptions
- **Structured Logging** for monitoring and debugging
- **Health Check Endpoints** for system monitoring
- **External API Integration** for importing cat facts
- **CORS Support** for frontend integration

## 📋 Prerequisites

- Python 3.8+
- Supabase account and project
- OpenAI API key (optional, for AI features)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   cd Meowlogy/Backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the Backend directory:
   ```env
   # Supabase Configuration
   SUPABASE_URL=your_supabase_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   
   # OpenAI Configuration (optional)
   OPENAI_API_KEY=your_openai_api_key
   
   # Server Configuration
   HOST=0.0.0.0
   PORT=8000
   DEBUG=False
   
   # Logging
   LOG_LEVEL=INFO
   
   # Validation Rules
   MAX_FACT_LENGTH=1000
   MIN_FACT_LENGTH=1
   MAX_IMPORT_FACTS=100
   DEFAULT_IMPORT_FACTS=5
   ```

## 🗄️ Database Setup

1. **Create Supabase tables** using the provided schema:
   ```sql
   -- Run the contents of supabase_schema.sql in your Supabase SQL editor
   ```

2. **Import initial data** (optional):
   ```bash
   python import_cat_facts.py
   ```

## 🏃‍♂️ Running the Application

### Development Mode
```bash
python main.py
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker (if available)
```bash
docker-compose up
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔌 API Endpoints

### Core Endpoints
- `GET /` - Root endpoint with API info
- `GET /health` - Health check
- `GET /catfacts` - Get all cat facts
- `GET /catfacts/random` - Get random cat fact
- `GET /catfacts/{fact_id}` - Get specific cat fact
- `POST /catfacts` - Add new cat fact
- `DELETE /catfacts/{fact_id}` - Soft delete cat fact

### Social Features
- `POST /catfacts/{fact_id}/like` - Like a cat fact
- `DELETE /catfacts/{fact_id}/like` - Unlike a cat fact

### AI Features
- `POST /api/ask-ai` - Get AI-powered cat care advice

### Utility Endpoints
- `POST /import-facts` - Import facts from external API

## 🏗️ Architecture Details

### 1. Configuration Management (`config.py`)
- Centralized configuration using environment variables
- Validation of required settings
- Logging setup
- CORS configuration

### 2. Constants (`constants.py`)
- All application constants in one place
- Error and success messages
- API configuration values
- Validation rules

### 3. Data Models (`Models/`)
- **Pydantic models** for request/response validation
- **Comprehensive schemas** with examples
- **Input validation** with custom validators
- **Type safety** throughout the application

### 4. Services Layer (`services/`)
- **Business logic separation** from API layer
- **CatFactsService**: Handles all cat fact operations
- **AIService**: Manages OpenAI interactions
- **Error handling** and logging

### 5. Database Layer (`supabase_db.py`)
- **Supabase client** initialization
- **CRUD operations** for cat facts
- **Error handling** and logging
- **Connection management**

### 6. Exception Handling (`exceptions.py`)
- **Custom exception classes** for different error types
- **Structured error handling** throughout the application
- **Consistent error responses**

## 🔧 Development

### Adding New Endpoints

1. **Create data models** in `Models/`
2. **Add business logic** in `services/`
3. **Create endpoint** in `main.py`
4. **Add error handling** and logging

### Example: Adding a new endpoint

```python
# In Models/cat_facts_models.py
class CatFactUpdateRequest(BaseModel):
    fact: str = Field(..., description="Updated fact text")

# In services/cat_facts_service.py
def update_fact(self, fact_id: str, fact: str) -> CatFactUpdateResponse:
    # Business logic here
    pass

# In main.py
@app.put("/catfacts/{fact_id}", response_model=CatFactUpdateResponse)
async def update_fact(
    fact_id: str,
    request: CatFactUpdateRequest,
    service: CatFactsService = Depends(get_cat_facts_service)
):
    # Endpoint implementation
    pass
```

## 🧪 Testing

### Manual Testing
Use the Swagger UI at `http://localhost:8000/docs` to test endpoints interactively.

### Example API Calls

```bash
# Get all facts
curl http://localhost:8000/catfacts

# Add a new fact
curl -X POST http://localhost:8000/catfacts \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "fact=Cats have over 20 muscles that control their ears"

# Get AI advice
curl -X POST http://localhost:8000/api/ask-ai \
  -H "Content-Type: application/json" \
  -d '{"question": "How often should I feed my cat?"}'
```

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Logs
- Application logs are written to console and `app.log` (in debug mode)
- Log level can be configured via `LOG_LEVEL` environment variable

## 🔒 Security Considerations

- **Environment variables** for sensitive data
- **Input validation** on all endpoints
- **CORS configuration** for frontend security
- **Error message sanitization** to prevent information leakage

## 🚀 Deployment

### Environment Variables
Ensure all required environment variables are set in production.

### Database
- Use Supabase production instance
- Configure proper RLS (Row Level Security) policies
- Set up database backups

### Monitoring
- Enable application logging
- Set up health check monitoring
- Configure error alerting

## 🤝 Contributing

1. Follow the existing code structure
2. Add proper error handling and logging
3. Update data models as needed
4. Test thoroughly before submitting

## 📄 License

This project is part of the Meowlogy application. 