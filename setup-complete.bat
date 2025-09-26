@echo off
REM Complete Harvester Tracking Platform Setup Script

echo 🌾 Harvester Tracking Platform - Complete Setup
echo ================================================
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

REM Check Docker (optional)
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Docker not found. You can still run with SQLite.
    set DOCKER_AVAILABLE=false
) else (
    echo ✅ Docker detected
    set DOCKER_AVAILABLE=true
)

echo.
echo 🎯 Choose your setup method:
echo    1. SQLite Setup (Recommended - No Docker needed)
echo    2. Docker Setup (Full environment)
echo    3. Frontend Only (Demo mode)
echo.
set /p choice="Enter your choice (1, 2, or 3): "

if "%choice%"=="1" goto :sqlite_setup
if "%choice%"=="2" goto :docker_setup
if "%choice%"=="3" goto :frontend_only
echo ❌ Invalid choice. Using SQLite setup...
goto :sqlite_setup

:sqlite_setup
echo.
echo 🔧 Setting up with SQLite...
echo.

REM Backend setup
echo 📦 Installing backend dependencies...
cd backend
pip install -r requirements-minimal.txt
if %errorlevel% neq 0 (
    echo ❌ Backend installation failed
    pause
    exit /b 1
)

echo 🔧 Configuring SQLite database...
echo DATABASE_URL=sqlite:///./harvester_tracking.db > .env
echo SECRET_KEY=your-secret-key-change-in-production >> .env
echo ALGORITHM=HS256 >> .env
echo ACCESS_TOKEN_EXPIRE_MINUTES=30 >> .env
echo ALLOWED_ORIGINS=["http://localhost:3000"] >> .env

echo 🗄️ Running database migrations...
alembic upgrade head
if %errorlevel% neq 0 (
    echo ❌ Database migration failed
    pause
    exit /b 1
)

echo 🚀 Starting backend server...
start "Backend Server" cmd /k "uvicorn main:app --reload"
cd ..

REM Frontend setup
echo 📦 Installing frontend dependencies...
cd frontend
npm install
if %errorlevel% neq 0 (
    echo ❌ Frontend installation failed
    pause
    exit /b 1
)

echo 🚀 Starting frontend server...
start "Frontend Server" cmd /k "npm start"
cd ..

echo.
echo ✅ SQLite setup complete!
echo.
echo 🌐 Access the application:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Documentation: http://localhost:8000/docs
echo.
echo 📊 Default admin user will be created on first run
echo    Email: admin@harvester.com
echo    Password: admin123
echo.
goto :end

:docker_setup
if "%DOCKER_AVAILABLE%"=="false" (
    echo ❌ Docker is required for this setup
    echo 📥 Download Docker Desktop from: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo.
echo 🐳 Setting up with Docker...
echo.

REM Create environment files
if not exist backend\.env (
    echo 📝 Creating backend environment file...
    copy backend\env.example backend\.env
)

if not exist frontend\.env (
    echo 📝 Creating frontend environment file...
    copy frontend\env.example frontend\.env
)

echo 🔨 Building and starting services...
docker-compose up --build -d

echo ⏳ Waiting for services to be ready...
timeout /t 15 /nobreak >nul

echo 🗄️ Running database migrations...
docker-compose exec backend alembic upgrade head

echo.
echo ✅ Docker setup complete!
echo.
echo 🌐 Access the application:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Documentation: http://localhost:8000/docs
echo.
echo 🛠️ To stop: docker-compose down
echo 🛠️ To view logs: docker-compose logs -f
echo.
goto :end

:frontend_only
echo.
echo 🎨 Setting up frontend only (demo mode)...
echo.

cd frontend
npm install
if %errorlevel% neq 0 (
    echo ❌ Frontend installation failed
    pause
    exit /b 1
)

echo 🚀 Starting frontend demo...
echo.
echo 📱 Frontend will be available at: http://localhost:3000
echo 📱 Demo page: http://localhost:3000/demo
echo.
echo ⚠️  Note: Backend features will show connection errors
echo    To enable full functionality, run the complete setup
echo.
npm start
cd ..
goto :end

:end
echo.
echo 🎉 Setup complete! Check the URLs above to access your application.
echo.
pause
