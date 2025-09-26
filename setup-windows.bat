@echo off
REM Windows-specific setup script for Harvester Tracking Platform

echo 🚀 Setting up Harvester Tracking Platform on Windows...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python first.
    echo 📥 Download from: https://www.python.org/downloads/
    echo ⚠️  Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python detected
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    echo 📥 Download from: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js detected
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Docker not found. You can still run the frontend.
    echo 📥 Download Docker Desktop from: https://www.docker.com/products/docker-desktop/
    echo.
    echo 🎯 Proceeding with frontend-only setup...
    goto :frontend_only
)

echo ✅ Docker detected
echo.

REM Create environment files if they don't exist
if not exist backend\.env (
    echo 📝 Creating backend environment file...
    copy backend\env.example backend\.env
)

if not exist frontend\.env (
    echo 📝 Creating frontend environment file...
    copy frontend\env.example frontend\.env
)

REM Try to install backend dependencies
echo 🔨 Installing backend dependencies...
cd backend

REM Try different installation methods
echo 📦 Attempting to install with psycopg2-binary...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ⚠️  psycopg2-binary failed, trying alternative...
    pip install -r requirements-windows.txt
    if %errorlevel% neq 0 (
        echo ⚠️  PostgreSQL dependencies failed, using SQLite for development...
        pip install -r requirements-sqlite.txt
        echo 📝 Note: Using SQLite instead of PostgreSQL for development
    )
)

cd ..

REM Install frontend dependencies
echo 🔨 Installing frontend dependencies...
cd frontend
npm install
cd ..

REM Try to start with Docker
echo 🐳 Starting services with Docker...
docker-compose up --build -d

if %errorlevel% neq 0 (
    echo ⚠️  Docker failed, starting frontend only...
    goto :frontend_only
)

echo ✅ Setup complete with Docker!
echo.
echo 🌐 Access the application:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Documentation: http://localhost:8000/docs
echo.
goto :end

:frontend_only
echo 🎯 Starting frontend only...
cd frontend
echo.
echo 📱 Frontend will be available at: http://localhost:3000
echo 📱 Demo page: http://localhost:3000/demo
echo.
echo ⚠️  Note: Backend features will show connection errors
echo    To enable full functionality, install Docker Desktop
echo.
npm start

:end
echo.
echo 🛠️ Troubleshooting:
echo    - If psycopg2 fails: Install PostgreSQL or use SQLite version
echo    - If Docker fails: Install Docker Desktop
echo    - For full setup: Run setup.bat after installing Docker
echo.
pause

