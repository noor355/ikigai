# Ikigai Career Guidance System

An AI-powered career recommendation platform based on the Ikigai framework. The system learns from user interactions to provide increasingly personalized career suggestions aligned with their abilities, interests, values, and passions.

## 🚀 Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: React
- **ML Engine**: scikit-learn, TensorFlow
- **Authentication**: JWT

## 📋 Prerequisites

- Python 3.9+
- Node.js 14+
- Supabase Account (free at https://supabase.com)

## 🔧 Backend Setup with Supabase

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign up
2. Click "New Project" and create a new project
3. Wait for the project to initialize (5-10 minutes)

### Step 2: Get Database Connection String

1. In Supabase, go to **Project Settings** → **Database**
2. Look for "Connection pooling" section
3. Select **Session mode** (important for FastAPI)
4. Copy the connection string that looks like:
   ```
   postgresql://postgres.[project-id]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```

### Step 3: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```powershell
   cp .env.example .env
   ```

2. Replace the `DATABASE_URL` with your Supabase connection string:
   ```
   DATABASE_URL=postgresql://postgres.[project-id]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```

3. Update other values if needed:
   ```
   SECRET_KEY=your-super-secret-key-change-this-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   API_V1_STR=/api/v1
   PROJECT_NAME=Ikigai Career Guidance API
   BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
   ```

### Step 4: Install Dependencies

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 5: Run the Server

```powershell
python main.py
```

The API will start at `http://localhost:8000`

### Step 6: Access API Documentation

Open your browser and go to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user info

### User Profile
- `GET /api/v1/profile/` - Get user profile
- `PUT /api/v1/profile/` - Update user profile
- `POST /api/v1/profile/add-interest` - Add interest
- `POST /api/v1/profile/add-skill` - Add skill

### Daily Entries
- `POST /api/v1/daily-entries/` - Create daily entry
- `GET /api/v1/daily-entries/` - Get daily entries
- `GET /api/v1/daily-entries/{id}` - Get specific entry
- `PUT /api/v1/daily-entries/{id}` - Update entry
- `DELETE /api/v1/daily-entries/{id}` - Delete entry

### Recommendations
- `POST /api/v1/recommendations/generate` - Generate career recommendations
- `GET /api/v1/recommendations/` - Get user's recommendations
- `GET /api/v1/recommendations/{id}` - Get recommendation details
- `POST /api/v1/recommendations/refresh` - Refresh recommendations

## 🎯 Features

### 1. User Authentication
- Secure JWT-based authentication
- Password hashing with bcrypt
- Protected routes

### 2. User Profile Management
- Store abilities (skills, experience)
- Track interests and passions
- Record values and life goals

### 3. Daily Entry System
- Log daily activities
- Record learnings and challenges
- Track mood and interests explored
- More entries = more accurate recommendations

### 4. AI Recommendation Engine
- Matches user profile to 10+ careers
- Future-oriented career focus
- Weights: Skills (25%), Interests (25%), Values (25%), Passion (25%)
- Career data includes:
  - Required skills
  - Growth potential (High/Medium/Low)
  - Market demand
  - Salary ranges
  - Future-oriented flag

### 5. Adaptive Learning
- Recommendations improve as user adds daily entries
- System learns from user interactions
- Real-time accuracy tracking

## 📁 Project Structure

```
ikigai/
├── backend/
│   ├── config.py              # Configuration and settings
│   ├── database.py            # Database setup
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── security.py            # JWT and password handling
│   ├── main.py                # FastAPI app entry point
│   ├── ml_engine.py           # Career recommendation engine
│   ├── routes_auth.py         # Authentication routes
│   ├── routes_profile.py      # Profile routes
│   ├── routes_daily.py        # Daily entry routes
│   ├── routes_recommendations.py  # Recommendation routes
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment template
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
└── ml_engine/
    └── models/               # ML models directory
```

## 🤖 ML Engine Details

The recommendation engine uses:
- **TF-IDF Vectorization** for interest matching
- **Cosine Similarity** for career-interest alignment
- **Skill matching** with overlap calculation
- **Weighted scoring** combining all factors
- **Adaptive boosting** from daily entries

### Career Database
Currently includes 10+ future-oriented careers:
- AI/ML Engineer
- Data Scientist
- Cloud Architect
- Data Engineer
- UX/UI Designer
- Product Manager
- Cybersecurity Specialist
- Blockchain Developer
- Renewable Energy Engineer
- Biotechnology Specialist

## 🧪 Testing the API

```bash
# Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123"}'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Create daily entry
curl -X POST "http://localhost:8000/api/v1/daily-entries/" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"activities":["coding","learning ML"],"mood":"happy"}'

# Generate recommendations
curl -X POST "http://localhost:8000/api/v1/recommendations/generate" \
  -H "Authorization: Bearer <your-token>"
```

## 🌐 Frontend Setup

```powershell
cd frontend
npm install
npm start
```

Frontend will run at `http://localhost:3000`

## 📚 Ikigai Framework

The recommendation system is based on the Ikigai framework:
1. **Ability** (What you're good at) → Skills
2. **Interest** (What you love doing) → Interests & Passions
3. **Value** (What the world values) → Market demand & Growth
4. **Mission** (What the world needs) → Future-oriented careers

## 🔐 Security

- All endpoints require JWT authentication
- Passwords are hashed with bcrypt
- SQL injection protection via SQLAlchemy ORM
- CORS configured for frontend
- Environment variables for sensitive data

## 🚀 Deployment

### Deploying Backend

1. **Railway.app** (recommended)
   - Connect your GitHub repo
   - Set environment variables
   - Auto-deploys on push

2. **Render**
   - Simple deployment platform
   - Good free tier
   - PostgreSQL support via Supabase

3. **Vercel** (for frontend)
   - Optimized for React
   - Serverless functions

## 📝 Environment Variables

```
DATABASE_URL              # Supabase PostgreSQL URL
SECRET_KEY               # JWT secret key
ALGORITHM                # HS256
ACCESS_TOKEN_EXPIRE_MINUTES  # 30
API_V1_STR              # /api/v1
PROJECT_NAME            # Project name
BACKEND_CORS_ORIGINS    # Comma-separated origins
```

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Push to GitHub
5. Create a pull request

## 📄 License

MIT License

## 👨‍💻 Authors

- Generated as part of Ikigai Career Guidance System project

## 🆘 Troubleshooting

### Database Connection Error
- Verify your Supabase connection string is correct
- Check that Supabase project is active
- Ensure your IP is not blocked by Supabase firewall

### CORS Errors
- Add your frontend URL to `BACKEND_CORS_ORIGINS` in `.env`
- Restart the backend server

### Tables Not Created
- FastAPI automatically creates tables on startup
- Check Supabase SQL Editor to verify tables exist

## 📞 Support

For issues, check:
1. FastAPI docs: https://fastapi.tiangolo.com/
2. Supabase docs: https://supabase.com/docs
3. SQLAlchemy docs: https://docs.sqlalchemy.org/
