@echo off
echo 🌾 Starting Harvester Tracking Platform - Frontend Demo
echo.

echo ✅ Node.js detected: v24.8.0
echo ❌ Python not found - Backend will not be available
echo ❌ Docker not found - Full setup not available
echo.

echo 🚀 Starting frontend development server...
echo.
echo 📱 Frontend will be available at: http://localhost:3000
echo 📱 Demo page will be available at: http://localhost:3000/demo
echo.
echo ⚠️  Note: Backend features will show connection errors
echo    To enable full functionality, install Python and Docker
echo.

cd frontend
npm start
