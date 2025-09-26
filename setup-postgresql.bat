@echo off
REM PostgreSQL Setup Script for Harvester Tracking Platform

echo 🐘 Setting up Harvester Tracking Platform with PostgreSQL
echo ========================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python first.
    echo 📥 Download from: https://www.python.org/downloads/
    echo ⚠️  Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo ✅ Python detected

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    echo 📥 Download from: https://nodejs.org/
    pause
    exit /b 1
)
echo ✅ Node.js detected

REM Check PostgreSQL
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PostgreSQL is not installed. Please install PostgreSQL first.
    echo 📥 Download from: https://www.postgresql.org/download/windows/
    echo.
    echo 🔧 After installing PostgreSQL:
    echo    1. Set password for 'postgres' user
    echo    2. Add PostgreSQL bin directory to PATH
    echo    3. Restart your terminal
    pause
    exit /b 1
)
echo ✅ PostgreSQL detected

echo.
echo 🔧 Setting up PostgreSQL database...

REM Create database
echo 📊 Creating database 'harvester_tracking'...
createdb harvester_tracking
if %errorlevel% neq 0 (
    echo ⚠️  Database might already exist, continuing...
)

echo.
echo 📦 Installing backend dependencies...
cd backend

REM Try to install PostgreSQL requirements first
echo 🔨 Installing PostgreSQL requirements...
pip install -r requirements-postgresql.txt
if %errorlevel% neq 0 (
    echo ⚠️  PostgreSQL requirements failed, trying alternative installation...
    pip install --only-binary=all psycopg2-binary
    if %errorlevel% neq 0 (
        echo ❌ Failed to install PostgreSQL dependencies
        echo 💡 Try installing PostgreSQL development headers
        echo 📥 Download from: https://www.postgresql.org/download/windows/
        pause
        exit /b 1
    )
    echo 🔨 Installing remaining dependencies...
    pip install -r requirements.txt
)
if %errorlevel% neq 0 (
    echo ❌ Backend installation failed
    pause
    exit /b 1
)

echo.
echo 🔧 Configuring environment...
if not exist .env (
    echo 📝 Creating PostgreSQL environment file...
    copy .env.postgresql .env
) else (
    echo 📝 Updating existing environment file for PostgreSQL...
    echo DATABASE_URL=postgresql://postgres:password@localhost:5432/harvester_tracking > .env
    echo SECRET_KEY=your-secret-key-change-in-production >> .env
    echo ALGORITHM=HS256 >> .env
    echo ACCESS_TOKEN_EXPIRE_MINUTES=30 >> .env
    echo ALLOWED_ORIGINS=["http://localhost:3000"] >> .env
)

echo.
echo 🗄️ Running database migrations...
alembic upgrade head
if %errorlevel% neq 0 (
    echo ❌ Database migration failed
    echo 💡 Check if PostgreSQL is running and database exists
    pause
    exit /b 1
)

echo.
echo 🚀 Starting backend server...
start "Backend Server" cmd /k "uvicorn main:app --reload"
cd ..

REM Frontend setup
echo.
echo 📦 Installing frontend dependencies...
cd frontend
npm install
if %errorlevel% neq 0 (
    echo ❌ Frontend installation failed
    pause
    exit /b 1
)

echo.
echo 🚀 Starting frontend server...
start "Frontend Server" cmd /k "npm start"
cd ..

echo.
echo ✅ PostgreSQL setup complete!
echo.
echo 🌐 Access the application:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Documentation: http://localhost:8000/docs
echo.
echo 📊 Database: PostgreSQL (harvester_tracking)
echo    Host: localhost:5432
echo    User: postgres
echo    Password: password (change in production)
echo.
echo 🛠️ To stop servers: Close the terminal windows
echo 🛠️ To view logs: Check the terminal windows
echo.
pause

