# Development Guide

## Local Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Docker & Docker Compose (optional)

### Backend Development

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

5. **Set up database:**
   ```bash
   # Create PostgreSQL database
   createdb harvester_tracking
   
   # Run migrations
   alembic upgrade head
   ```

6. **Create admin user:**
   ```bash
   python scripts/create_admin.py
   ```

7. **Start the server:**
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Development

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your API URL
   ```

4. **Start the development server:**
   ```bash
   npm start
   ```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `name`: Full name
- `hashed_password`: Bcrypt hashed password
- `state`: US state for peer comparisons
- `billing_method`: per_acre, per_bushel, or per_hour
- `equipment_owned`: Boolean flag
- `equipment_details`: Text description
- `is_active`: Account status
- `is_admin`: Admin privileges
- `created_at`, `updated_at`: Timestamps

### Income Entries Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `acres_harvested`: Number of acres
- `rate_per_unit`: Rate per acre/bushel/hour
- `total_earned`: Total income
- `client_name`: Optional client name
- `notes`: Optional notes
- `harvest_date`: Date of harvest
- `created_at`, `updated_at`: Timestamps

### Expense Entries Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `category`: Expense category (fuel, labor, etc.)
- `amount`: Expense amount
- `description`: Optional description
- `notes`: Optional notes
- `expense_date`: Date of expense
- `created_at`, `updated_at`: Timestamps

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Deployment

1. **Backend:**
   - Set up PostgreSQL database
   - Configure environment variables
   - Run migrations: `alembic upgrade head`
   - Start with: `uvicorn main:app --host 0.0.0.0 --port 8000`

2. **Frontend:**
   - Build: `npm run build`
   - Serve with nginx or similar web server

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/harvester_tracking
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=["http://localhost:3000"]
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **Database connection errors:**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Verify database exists

2. **CORS errors:**
   - Check ALLOWED_ORIGINS in backend .env
   - Ensure frontend URL is included

3. **Authentication issues:**
   - Check SECRET_KEY is set
   - Verify JWT token expiration settings

4. **Frontend build errors:**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility
