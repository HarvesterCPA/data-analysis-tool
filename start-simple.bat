@echo off
echo 🌾 Starting Harvester Tracking Platform - Simple Setup
echo.

echo 📦 Installing minimal requirements...
cd backend
pip install -r requirements-minimal.txt

echo.
echo 🔧 Setting up SQLite database...
echo DATABASE_URL=sqlite:///./harvester_tracking.db > .env
echo SECRET_KEY=your-secret-key-change-in-production >> .env
echo ALGORITHM=HS256 >> .env
echo ACCESS_TOKEN_EXPIRE_MINUTES=30 >> .env
echo ALLOWED_ORIGINS=["http://localhost:3000"] >> .env

echo.
echo 🗄️ Running database migrations...
alembic upgrade head

echo.
echo 🚀 Starting backend server...
echo 📡 Backend will be available at: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo.
echo ⚠️  Note: This uses SQLite instead of PostgreSQL
echo    For production, install PostgreSQL and use the full setup
echo.

uvicorn main:app --reload
