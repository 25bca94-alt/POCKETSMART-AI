# =========================================================
# PocketSmartAI Environment Configuration
# =========================================================

# Application
APP_NAME=PocketSmartAI
APP_VERSION=1.0.0
DEBUG=true

# Database
DATABASE_URL=sqlite:///./pocketsmart.db

# JWT Authentication
SECRET_KEY=replace-this-with-a-long-random-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Google Gemini API
# Get your API key from Google AI Studio.
GEMINI_API_KEY=your_gemini_api_key_here