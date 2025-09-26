@echo off
REM Docker PostgreSQL Setup Script for Harvester Tracking Platform

echo 🐘 Setting up Harvester Tracking Platform with Docker + PostgreSQL
echo =================================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker first.
    echo 📥 Download from: https://www.docker.com/products/docker-desktop/
    echo.
    echo 🎯 Alternative: Use local PostgreSQL setup
    echo    Run: setup-postgresql.bat
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    echo 📥 Download from: https://www.docker.com/products/docker-desktop/
    echo.
    echo 🎯 Alternative: Use local PostgreSQL setup
    echo    Run: setup-postgresql.bat
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed

REM Create environment files if they don't exist
if not exist backend\.env (
    echo 📝 Creating backend environment file...
    copy backend\env.example backend\.env
)

if not exist frontend\.env (
    echo 📝 Creating frontend environment file...
    copy frontend\env.example frontend\.env
)

REM Build and start services
echo 🔨 Building and starting services with PostgreSQL...
docker-compose up --build -d

REM Wait for database to be ready
echo ⏳ Waiting for PostgreSQL to be ready...
timeout /t 15 /nobreak >nul

REM Run database migrations
echo 🗄️ Running database migrations...
docker-compose exec backend alembic upgrade head

echo ✅ Setup complete!
echo.
echo 🌐 Access the application:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Documentation: http://localhost:8000/docs
echo.
echo 📊 Database: PostgreSQL (Docker)
echo    Host: localhost:5432
echo    Database: harvester_tracking
echo    User: postgres
echo    Password: password
echo.
echo 📊 Default admin user will be created on first run
echo    Email: admin@harvester.com
echo    Password: admin123
echo.
echo 🛠️ To stop the services: docker-compose down
echo 🛠️ To view logs: docker-compose logs -f
echo.
echo 💡 For local PostgreSQL setup: setup-postgresql.bat
echo 💡 For PostgreSQL installation guide: POSTGRESQL_SETUP.md
echo.
pause

