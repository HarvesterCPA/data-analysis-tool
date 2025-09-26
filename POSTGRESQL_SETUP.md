# PostgreSQL Setup Guide

## 🐘 Installing PostgreSQL on Windows

### Step 1: Download PostgreSQL
1. Go to https://www.postgresql.org/download/windows/
2. Click "Download the installer"
3. Download the latest version (13+ recommended)

### Step 2: Install PostgreSQL
1. Run the downloaded installer
2. **Important**: During installation:
   - Set password for 'postgres' user (remember this password!)
   - **Check "Add PostgreSQL bin directory to PATH"**
   - Choose port 5432 (default)
   - Choose locale (default is fine)

### Step 3: Verify Installation
```bash
# Open a new terminal/command prompt
psql --version
```

If you get "command not found", add PostgreSQL to your PATH:
1. Find PostgreSQL installation directory (usually `C:\Program Files\PostgreSQL\13\bin`)
2. Add it to your system PATH environment variable

### Step 4: Test Connection
```bash
# Connect to PostgreSQL
psql -U postgres -h localhost

# You'll be prompted for the password you set during installation
# Once connected, you can exit with: \q
```

## 🔧 Setting Up the Database

### Method 1: Using the Setup Script (Recommended)
```bash
# Run the PostgreSQL setup script
setup-postgresql.bat
```

### Method 2: Manual Setup
```bash
# 1. Create the database
createdb harvester_tracking

# 2. Install backend dependencies
cd backend
pip install -r requirements.txt

# 3. Run migrations
alembic upgrade head

# 4. Start the backend
uvicorn main:app --reload
```

## 🐳 Using Docker (Alternative)

If you prefer not to install PostgreSQL locally:

```bash
# Start PostgreSQL with Docker
docker run --name postgres-harvester -e POSTGRES_PASSWORD=password -e POSTGRES_DB=harvester_tracking -p 5432:5432 -d postgres:13

# Then run the backend
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

## 🔍 Troubleshooting

### Common Issues

#### 1. "psql: command not found"
**Solution**: Add PostgreSQL bin directory to PATH
- Find PostgreSQL installation (usually `C:\Program Files\PostgreSQL\13\bin`)
- Add to system PATH environment variable
- Restart terminal

#### 2. "psycopg2 installation failed"
**Solutions**:
```bash
# Try pre-compiled binary
pip install --only-binary=all psycopg2-binary

# Or install PostgreSQL development headers
# Download from: https://www.postgresql.org/download/windows/
# Make sure to install with development tools
```

#### 3. "Database does not exist"
**Solution**:
```bash
# Create the database
createdb harvester_tracking

# Or connect to PostgreSQL and create manually
psql -U postgres -h localhost
CREATE DATABASE harvester_tracking;
\q
```

#### 4. "Connection refused"
**Solutions**:
- Make sure PostgreSQL service is running
- Check if port 5432 is available
- Verify firewall settings
- Try connecting with: `psql -U postgres -h localhost`

#### 5. "Authentication failed"
**Solution**:
- Check the password you set during PostgreSQL installation
- Try resetting postgres user password:
```bash
# Connect as superuser and reset password
psql -U postgres -h localhost
ALTER USER postgres PASSWORD 'newpassword';
\q
```

## 🔐 Security Notes

### Production Setup
For production, change these defaults:
- **Password**: Use a strong password for postgres user
- **Port**: Consider using a different port
- **Host**: Restrict access to localhost only
- **SSL**: Enable SSL connections

### Environment Variables
Update your `.env` file for production:
```env
DATABASE_URL=postgresql://username:strongpassword@localhost:5432/harvester_tracking
SECRET_KEY=your-very-secure-secret-key-here
```

## 📊 Database Management

### Useful Commands
```bash
# Connect to database
psql -U postgres -d harvester_tracking

# List all databases
\l

# List all tables
\dt

# Describe a table
\d table_name

# Exit psql
\q
```

### Backup and Restore
```bash
# Backup database
pg_dump -U postgres harvester_tracking > backup.sql

# Restore database
psql -U postgres harvester_tracking < backup.sql
```

## 🎯 Quick Test

After setup, test your installation:

```bash
# 1. Test PostgreSQL connection
psql -U postgres -d harvester_tracking -c "SELECT version();"

# 2. Test backend connection
cd backend
python -c "from app.core.database import engine; print('Database connection OK')"

# 3. Run migrations
alembic upgrade head

# 4. Start backend
uvicorn main:app --reload
```

If all steps work, you're ready to go! 🎉

