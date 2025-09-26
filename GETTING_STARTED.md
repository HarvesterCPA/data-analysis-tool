# Getting Started Guide

## 🚀 Quick Start (Choose Your Method)

### Method 1: Complete Setup (Recommended)
```bash
# Run the complete setup script
setup-complete.bat
```
This will guide you through the entire setup process.

### Method 2: SQLite Only (Fastest)
```bash
# Backend with SQLite
start-backend-sqlite.bat

# Frontend (in another terminal)
cd frontend
npm install
npm start
```

### Method 3: Docker (Full Environment)
```bash
# Requires Docker Desktop
setup.bat
```

## 📋 Prerequisites

### Required
- **Python 3.8+** (Python 3.13 supported)
- **Node.js 16+**

### Optional
- **Docker Desktop** (for full containerized setup)
- **PostgreSQL** (for production database)

## 🔧 Installation Steps

### Step 1: Clone/Download Project
```bash
# If using Git
git clone <repository-url>
cd harvester-tracking

# Or download and extract the ZIP file
```

### Step 2: Choose Your Setup Method

#### Option A: SQLite Setup (Easiest)
```bash
# Backend
cd backend
pip install -r requirements-minimal.txt
alembic upgrade head
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm start
```

#### Option B: PostgreSQL Setup
```bash
# Install PostgreSQL first
# Then:
cd backend
pip install -r requirements.txt
# Create database: createdb harvester_tracking
alembic upgrade head
uvicorn main:app --reload
```

#### Option C: Docker Setup
```bash
# Install Docker Desktop first
# Then:
docker-compose up --build -d
```

## 🌐 Access Points

Once running, you can access:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Demo Page**: http://localhost:3000/demo

## 🔑 Default Credentials

- **Admin Email**: admin@harvester.com
- **Admin Password**: admin123

## 🛠️ Troubleshooting

### Common Issues

#### 1. Python Not Found
```bash
# Install Python from https://www.python.org/downloads/
# Make sure to check "Add Python to PATH" during installation
```

#### 2. Node.js Not Found
```bash
# Install Node.js from https://nodejs.org/
```

#### 3. psycopg2 Installation Error
```bash
# Use SQLite instead (easier)
pip install -r requirements-minimal.txt
```

#### 4. Port Already in Use
```bash
# Find and kill process using port
netstat -ano | findstr :3000
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

#### 5. Database Connection Error
```bash
# For SQLite: Check if .env file exists
# For PostgreSQL: Ensure PostgreSQL is running
```

## 📊 Database Options

### SQLite (Development - Default)
- **Pros**: No setup required, works out of the box
- **Cons**: Not suitable for production
- **File**: `harvester_tracking.db` in backend directory

### PostgreSQL (Production)
- **Pros**: Production-ready, better performance
- **Cons**: Requires installation and setup
- **Setup**: Install PostgreSQL, create database

## 🎯 Development Workflow

### Backend Development
```bash
cd backend
# Install dependencies
pip install -r requirements-minimal.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
# Install dependencies
npm install

# Start development server
npm start
```

### Full Stack Development
```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm start
```

## 🚀 Production Deployment

### Using Docker
```bash
# Build production images
docker-compose -f docker-compose.prod.yml up --build -d
```

### Manual Deployment
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run build
# Serve with nginx or similar
```

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **Troubleshooting Guide**: TROUBLESHOOTING.md
- **Development Guide**: DEVELOPMENT.md
- **API Reference**: API.md

## 🆘 Need Help?

1. **Check the troubleshooting guide**: TROUBLESHOOTING.md
2. **Review the API documentation**: API.md
3. **Check the development guide**: DEVELOPMENT.md
4. **Run the complete setup**: setup-complete.bat

## 🎉 Success!

Once everything is running, you should see:
- Frontend at http://localhost:3000
- Backend API at http://localhost:8000
- API docs at http://localhost:8000/docs

Happy coding! 🌾
