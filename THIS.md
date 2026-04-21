# THIS.md
# Project memory file — maintained by Copilot
# Do not edit manually unless correcting something wrong
# Last updated: April 21, 2026

---

## Project Overview
- **Name:** Ikigai Career Guidance System
- **What it does:** An AI-powered career recommendation platform based on the Ikigai framework. Users log daily activities, learnings, and challenges. The system analyzes their input using NLP and ML to provide personalized career recommendations aligned with their abilities, interests, values, and passions.
- **Who it's for:** Students and professionals seeking career guidance
- **Current stage:** MVP in progress
- **Deadline or timeline:** Not specified

---

## Stack
*(Update this immediately whenever the stack changes — see Stack Change Protocol)*

| Layer | Technology | Reason chosen |
|-------|-----------|---------------|
| Frontend | React + CSS | Component-based, interactive UI for journal and recommendations |
| Backend | FastAPI (Python) | Fast, modern, native async support for ML/NLP tasks |
| Database | Supabase (PostgreSQL) | Managed PostgreSQL, free tier suitable for MVP, built-in auth |
| Auth | JWT + PassLib/Bcrypt | Stateless auth, secure password hashing |
| ML Engine | scikit-learn, TensorFlow | Industry-standard for ML recommendations |
| NLP Engine | HuggingFace Transformers, Sentence Transformers | State-of-the-art for text understanding and semantic analysis |
| Other | Celery + Redis, Gunicorn | Task queue for async ML processing, production-ready deployment |

---

## Folder Structure
*(Update as structure evolves)*

```
/
├── backend/
│   ├── ml_engine/
│   │   ├── nlp_processor.py          (Text analysis and sentiment)
│   │   ├── recommendation_engine.py  (Career matching algorithm)
│   │   ├── career_database.py        (Career data storage)
│   │   ├── service.py                (ML orchestration)
│   │   └── nlp_integration_examples.py
│   ├── routes_auth.py                (Authentication endpoints)
│   ├── routes_chat.py                (Chat/messaging)
│   ├── routes_daily.py               (Journal entries)
│   ├── routes_profile.py             (User profile)
│   ├── routes_recommendations.py     (Career recommendations)
│   ├── models.py                     (Database models)
│   ├── schemas.py                    (Pydantic validators)
│   ├── database.py                   (Supabase connection)
│   ├── security.py                   (JWT and auth helpers)
│   ├── config.py                     (Configuration management)
│   ├── main.py                       (FastAPI app entry)
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   └── Layout.js
│   │   ├── pages/
│   │   │   ├── AuthPage.js           (Login/signup)
│   │   │   ├── ChatPage.js           (Chat interface)
│   │   │   ├── DashboardPage.js      (Overview)
│   │   │   ├── JournalPage.js        (Daily journal entry)
│   │   │   ├── RecommendationsPage.js (Career recommendations)
│   │   │   ├── JournalHistoryPage.js (Past entries)
│   │   │   └── TestsPage.js          (Testing/QA)
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── .env                              (DO NOT COMMIT)
├── .gitignore
├── package.json
├── run-all.bat
├── THIS.md
├── COPILOT_INSTRUCTIONS.md
└── README.md
```

---

## Conventions
- **Variable naming:** camelCase (JavaScript), snake_case (Python)
- **Component naming:** PascalCase (React components)
- **API prefix:** /api/v1/
- **State management:** React hooks (Context/useState)
- **CSS approach:** CSS files per component (scoped styling)
- **Error handling:** try/catch in FastAPI endpoints, global error middleware, async error handling

---

## Environment Variables
*(List variable names only — never values)*
- `DATABASE_URL` (Supabase PostgreSQL connection string)
- `JWT_SECRET` (Secret key for token signing)
- `JWT_ALGORITHM` (e.g., HS256)
- `CORS_ORIGINS` (Allowed frontend URLs)
- `ENVIRONMENT` (development/production)

---

## Current Status
*(Updated by Copilot at end of every session)*

**Working:**
- ✅ Authentication (JWT-based login/signup)
- ✅ User profiles with Ikigai assessment
- ✅ Daily journal page with activities, learnings, challenges, mood tracking
- ✅ Recommendations display with career matching
- ✅ NLP integration for text analysis
- ✅ ML recommendation engine (basic)

**Broken or incomplete:**
- [ ] API endpoint testing (needs unit tests)
- [ ] Frontend error boundaries
- [ ] Database migrations (Alembic setup)

**Next up:**
- [ ] Integration testing
- [ ] Performance optimization for NLP
- [ ] Dashboard analytics

---

## Decisions Log
*(Copilot adds a row whenever a significant decision is made)*

| Date | Decision | Reason |
|------|----------|--------|
| Apr 21, 2026 | Created THIS.md to establish project memory and workflow | Standardize context management and session tracking per COPILOT_INSTRUCTIONS |

---

## Known Issues / Watch Out For
- Supabase free tier may have connection limits — monitor during scaling
- TensorFlow is heavy, consider lazy-loading if startup time becomes an issue
- HuggingFace model downloads happen on first run — can be slow, consider pre-downloading

---

## Session History
*(One line per session, added by Copilot)*

| Date | Summary |
|------|---------|
| Apr 21, 2026 | Initialized THIS.md for ikigai project. Reviewed existing stack: FastAPI + React + Supabase + HuggingFace NLP. Project at MVP stage with journal and recommendations working. |
