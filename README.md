# Harvester Income Tracking Platform

A web platform built with FastAPI (backend) and React (frontend) that allows custom harvesters to track their income, expenses, and profit/loss with peer comparisons.

## Features

### Phase 1 (MVP)
- User authentication (register, login, password reset)
- Personal profile setup with billing methods and location
- Income and expense tracking
- Dashboard with profit/loss summary
- Basic peer comparison (state + national level)
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
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Database Setup
```bash
# Create PostgreSQL database
createdb harvester_tracking

# Run migrations
cd backend
alembic upgrade head
```

## API Documentation
Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Development
- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:3000`
- Database runs on `localhost:5432`