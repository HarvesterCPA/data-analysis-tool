# Troubleshooting Guide

## Common Issues and Solutions

### 1. psycopg2-binary Installation Error

**Error**: `Error: pg_config executable not found`

**Solutions**:

#### Option A: Use Alternative Requirements (Recommended)
```bash
cd backend
pip install -r requirements-windows.txt
```

#### Option B: Use SQLite for Development
```bash
cd backend
pip install -r requirements-sqlite.txt
```

#### Option C: Install PostgreSQL Development Headers
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Install with development tools
3. Add PostgreSQL bin directory to PATH
4. Try installing again: `pip install -r requirements.txt`

#### Option D: Use Pre-compiled Wheels
```bash
pip install --only-binary=all psycopg2-binary
```

### 2. Python Not Found

**Error**: `python is not recognized`

**Solution**:
1. Download Python from https://www.python.org/downloads/
2. **Important**: Check "Add Python to PATH" during installation
3. Restart your terminal
4. Verify: `python --version`

### 3. Node.js Not Found

**Error**: `node is not recognized`

**Solution**:
1. Download Node.js from https://nodejs.org/
2. Install with default settings
3. Restart your terminal
4. Verify: `node --version`

### 4. Docker Not Found

**Error**: `docker is not recognized`

**Solution**:
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop/
2. Install and restart your computer
3. Start Docker Desktop
4. Verify: `docker --version`

### 5. Database Connection Issues

**Error**: `database connection failed`

**Solutions**:

#### For PostgreSQL:
1. Install PostgreSQL
2. Create database: `createdb harvester_tracking`
3. Update `DATABASE_URL` in `backend/.env`

#### For SQLite (Development):
1. Use `requirements-sqlite.txt`
2. Update `DATABASE_URL` to: `sqlite:///./harvester_tracking.db`

### 6. Frontend Build Errors

**Error**: `npm install` fails

**Solutions**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules
npm install

# Or use yarn instead
yarn install
```

### 7. CORS Errors

**Error**: `CORS policy` errors in browser

**Solution**:
1. Check `ALLOWED_ORIGINS` in `backend/.env`
2. Ensure frontend URL is included
3. Restart backend server

### 8. Port Already in Use

**Error**: `Port 3000/8000 already in use`

**Solutions**:
```bash
# Find process using port
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <process_id> /F

# Or use different ports
# Frontend: PORT=3001 npm start
# Backend: uvicorn main:app --port 8001
```

## Quick Fixes

### Windows-Specific Setup
```bash
# Use the Windows setup script
setup-windows.bat
```

### Frontend Only (No Backend)
```bash
cd frontend
npm install
npm start
# Visit http://localhost:3000/demo
```

### Backend Only (No Frontend)
```bash
cd backend
pip install -r requirements-sqlite.txt
uvicorn main:app --reload
# Visit http://localhost:8000/docs
```

## Environment Variables

### Backend (.env)
```env
# For PostgreSQL
DATABASE_URL=postgresql://postgres:password@localhost:5432/harvester_tracking

# For SQLite (development)
DATABASE_URL=sqlite:///./harvester_tracking.db

SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=["http://localhost:3000"]
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
```

## Still Having Issues?

1. **Check Python version**: `python --version` (should be 3.8+)
2. **Check Node.js version**: `node --version` (should be 16+)
3. **Check Docker**: `docker --version`
4. **Check ports**: Make sure 3000 and 8000 are available
5. **Check firewall**: Ensure ports aren't blocked
6. **Check antivirus**: Some antivirus software blocks development servers

## Alternative Setup Methods

### Method 1: Docker Only
```bash
# If you have Docker, this is the easiest
docker-compose up --build -d
```

### Method 2: Manual Setup
```bash
# Backend
cd backend
pip install -r requirements-sqlite.txt
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm start
```

### Method 3: Development with SQLite
```bash
# Use SQLite instead of PostgreSQL
cd backend
pip install -r requirements-sqlite.txt
# Update .env to use SQLite
# Run migrations
alembic upgrade head
uvicorn main:app --reload
```

