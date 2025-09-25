# Quick Start Guide

## Current Environment Status
✅ Node.js v24.8.0 - Available  
❌ Python - Not installed  
❌ Docker - Not installed  

## Option 1: Frontend Only (Immediate)

Since you have Node.js, you can run the frontend immediately:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will run on http://localhost:3000

**Note**: The frontend will show connection errors since the backend isn't running, but you can see the UI and interface.

## Option 2: Full Setup (Recommended)

### Step 1: Install Python
1. Go to https://www.python.org/downloads/
2. Download Python 3.8+ for Windows
3. **Important**: During installation, check "Add Python to PATH"
4. Restart your terminal after installation

### Step 2: Install Docker Desktop
1. Go to https://www.docker.com/products/docker-desktop/
2. Download Docker Desktop for Windows
3. Install and restart your computer
4. Start Docker Desktop

### Step 3: Run the Project
```bash
# Windows
setup.bat

# Or manually:
docker-compose up --build -d
```

## Option 3: Manual Backend Setup (Without Docker)

If you prefer not to use Docker:

### Install Python Dependencies
```bash
# After installing Python
cd backend
pip install -r requirements.txt
```

### Install PostgreSQL
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Install with default settings
3. Create database: `createdb harvester_tracking`

### Run Backend
```bash
cd backend
# Set up environment
copy env.example .env
# Edit .env with your database credentials

# Run migrations
alembic upgrade head

# Start server
uvicorn main:app --reload
```

### Run Frontend
```bash
cd frontend
npm install
npm start
```

## Troubleshooting

### Python Not Found
- Make sure Python is added to PATH during installation
- Restart your terminal after installing Python
- Try using `py` instead of `python` on Windows

### Docker Not Found
- Install Docker Desktop
- Make sure Docker Desktop is running
- Restart your computer after installation

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in backend/.env file
- Verify database exists: `createdb harvester_tracking`

## Next Steps

1. **For immediate testing**: Run the frontend only (Option 1)
2. **For full functionality**: Install Python and Docker (Option 2)
3. **For development**: Use manual setup (Option 3)

The project is fully functional once you have the required dependencies installed!
