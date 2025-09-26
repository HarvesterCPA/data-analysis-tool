# Harvester Income Tracking Platform

A web platform built with FastAPI (backend) and React (frontend) that allows custom harvesters to track their income, expenses, and profit/loss with peer comparisons.

## Features

### Phase 1 (MVP)
- User authentication (register, login, password reset)
- Personal profile setup with billing methods and location
- Income and expense tracking
- Dashboard with profit/loss summary
- Basic peer comparison (state, crop + national level)
- Admin panel for user management

### Tech Stack
- **Backend**: Python FastAPI
- **Frontend**: React with TypeScript
- **Database**: PostgreSQL
- **Authentication**: JWT tokens
- **UI Framework**: Material-UI (MUI)

## Project Structure

```
harvester-tracking/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── alembic/            # Database migrations
│   ├── requirements.txt
│   └── main.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── hooks/         # Custom hooks
│   │   ├── types/         # TypeScript types
│   │   └── utils/         # Utilities
│   ├── package.json
│   └── public/
└── docker-compose.yml      # Development environment
```

## Quick Start

### Prerequisites
- Python 3.8+ (Python 3.13 supported)
- Node.js 16+
- PostgreSQL 12+

### PostgreSQL Setup
```bash
# Install PostgreSQL first
# Download from: https://www.postgresql.org/download/windows/

# Backend with PostgreSQL
cd backend
pip install -r requirements.txt
# Create PostgreSQL database
createdb harvester_tracking
alembic upgrade head
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Quick Start Scripts
```bash
# Windows - PostgreSQL setup
setup-postgresql.bat

# Windows - Full setup with Docker
setup.bat
```

## 🚀 Quick Start

### Easiest Method (PostgreSQL)
```bash
# Run the PostgreSQL setup
setup-postgresql.bat
```

### Manual Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
createdb harvester_tracking
alembic upgrade head
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm start
```

## API Documentation
Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Development
- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:3000`
- Database runs on `localhost:5432`