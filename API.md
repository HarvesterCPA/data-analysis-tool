# API Documentation

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### Authentication

#### POST /api/auth/register
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "password123",
  "state": "California",
  "billing_method": "per_acre",
  "equipment_owned": true,
  "equipment_details": "John Deere 9870"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "state": "California",
  "billing_method": "per_acre",
  "equipment_owned": true,
  "equipment_details": "John Deere 9870",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### POST /api/auth/login
Login with email and password.

**Request Body (form-data):**
```
username: user@example.com
password: password123
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### GET /api/auth/me
Get current user information.

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "state": "California",
  "billing_method": "per_acre",
  "equipment_owned": true,
  "equipment_details": "John Deere 9870",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Users

#### GET /api/users/me
Get current user profile.

#### PUT /api/users/me
Update current user profile.

**Request Body:**
```json
{
  "name": "John Smith",
  "state": "Texas",
  "billing_method": "per_bushel",
  "equipment_owned": false,
  "equipment_details": "Leased equipment"
}
```

### Income Entries

#### GET /api/income/
Get income entries for current user.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records (default: 100)
- `start_date`: Filter from date (YYYY-MM-DD)
- `end_date`: Filter to date (YYYY-MM-DD)

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "acres_harvested": 100.5,
    "rate_per_unit": 25.00,
    "total_earned": 2512.50,
    "client_name": "Smith Farm",
    "notes": "Wheat harvest",
    "harvest_date": "2024-01-15T00:00:00Z",
    "created_at": "2024-01-15T10:00:00Z"
  }
]
```

#### POST /api/income/
Create new income entry.

**Request Body:**
```json
{
  "acres_harvested": 100.5,
  "rate_per_unit": 25.00,
  "total_earned": 2512.50,
  "client_name": "Smith Farm",
  "notes": "Wheat harvest",
  "harvest_date": "2024-01-15T00:00:00Z"
}
```

#### GET /api/income/{income_id}
Get specific income entry.

#### PUT /api/income/{income_id}
Update income entry.

#### DELETE /api/income/{income_id}
Delete income entry.

### Expense Entries

#### GET /api/expenses/
Get expense entries for current user.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records (default: 100)
- `start_date`: Filter from date (YYYY-MM-DD)
- `end_date`: Filter to date (YYYY-MM-DD)
- `category`: Filter by expense category

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "category": "fuel",
    "amount": 150.00,
    "description": "Diesel fuel",
    "notes": "Weekly fuel purchase",
    "expense_date": "2024-01-15T00:00:00Z",
    "created_at": "2024-01-15T10:00:00Z"
  }
]
```

#### POST /api/expenses/
Create new expense entry.

**Request Body:**
```json
{
  "category": "fuel",
  "amount": 150.00,
  "description": "Diesel fuel",
  "notes": "Weekly fuel purchase",
  "expense_date": "2024-01-15T00:00:00Z"
}
```

**Expense Categories:**
- `fuel`: Fuel costs
- `labor`: Labor costs
- `equipment_lease`: Equipment leasing
- `equipment_repair`: Equipment repairs
- `equipment_depreciation`: Equipment depreciation
- `rent_interest`: Rent and interest
- `taxes`: Tax expenses
- `other`: Other expenses

#### GET /api/expenses/{expense_id}
Get specific expense entry.

#### PUT /api/expenses/{expense_id}
Update expense entry.

#### DELETE /api/expenses/{expense_id}
Delete expense entry.

### Analytics

#### GET /api/analytics/dashboard
Get dashboard analytics for current user.

**Query Parameters:**
- `start_date`: Analysis start date (YYYY-MM-DD)
- `end_date`: Analysis end date (YYYY-MM-DD)

**Response:**
```json
{
  "profit_loss": {
    "total_income": 5000.00,
    "total_expenses": 3500.00,
    "profit_loss": 1500.00,
    "period_start": "2024-01-01T00:00:00Z",
    "period_end": "2024-01-31T23:59:59Z"
  },
  "expense_breakdown": [
    {
      "category": "fuel",
      "amount": 1000.00,
      "percentage": 28.57
    },
    {
      "category": "labor",
      "amount": 1500.00,
      "percentage": 42.86
    }
  ],
  "peer_comparisons": [
    {
      "metric": "Income per Harvest",
      "user_value": 2500.00,
      "state_average": 2200.00,
      "national_average": 2100.00,
      "state_percentile": 75,
      "national_percentile": 80
    }
  ],
  "insights": [
    "Great job! You're operating at a profit.",
    "Your fuel costs are high. Consider fuel efficiency improvements."
  ]
}
```

### Admin (Admin Only)

#### GET /api/admin/users
Get all users (admin only).

#### GET /api/admin/stats
Get platform statistics (admin only).

**Response:**
```json
{
  "total_users": 150,
  "active_users": 145,
  "total_income_entries": 1250,
  "total_expense_entries": 2100,
  "total_income_tracked": 2500000.00,
  "total_expenses_tracked": 1800000.00
}
```

#### DELETE /api/admin/users/{user_id}
Deactivate user (admin only).

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Rate Limiting

API requests are not currently rate-limited, but this may be implemented in production.

## CORS

The API supports CORS for the following origins:
- `http://localhost:3000` (development)
- Configure additional origins in the `ALLOWED_ORIGINS` environment variable
