@echo off
echo 🧪 Testing Harvester Tracking Platform Setup
echo =============================================
echo.

REM Test Python
echo 🔍 Testing Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found
    exit /b 1
)
echo ✅ Python OK

REM Test Node.js
echo 🔍 Testing Node.js...
node --version
if %errorlevel% neq 0 (
    echo ❌ Node.js not found
    exit /b 1
)
echo ✅ Node.js OK

REM Test backend dependencies
echo 🔍 Testing backend dependencies...
cd backend
python -c "import fastapi, sqlalchemy, alembic; print('✅ Backend dependencies OK')"
if %errorlevel% neq 0 (
    echo ❌ Backend dependencies missing
    echo 💡 Run: pip install -r requirements-minimal.txt
    exit /b 1
)
cd ..

REM Test frontend dependencies
echo 🔍 Testing frontend dependencies...
cd frontend
if exist node_modules (
    echo ✅ Frontend dependencies OK
) else (
    echo ❌ Frontend dependencies missing
    echo 💡 Run: npm install
    exit /b 1
)
cd ..

REM Test database file
echo 🔍 Testing database configuration...
if exist backend\.env (
    echo ✅ Environment file exists
) else (
    echo ⚠️  Environment file missing
    echo 💡 Run: copy backend\env.example backend\.env
)

echo.
echo 🎉 Setup test complete!
echo.
echo 🚀 Ready to start:
echo    Backend: cd backend && uvicorn main:app --reload
echo    Frontend: cd frontend && npm start
echo.
pause
