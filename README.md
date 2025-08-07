# Agnovat Support Worker Management System

A Django-based web application for managing support workers, scheduling, compliance, incident reporting, and behavioral analysis for individuals with autism and intellectual disability.

## Features

- **Role-based Authentication**: Admin, Support Worker, Coordinator, and Behaviour Practitioner roles
- **JWT Authentication**: Secure token-based authentication
- **User Management**: Custom user model with role-based access control
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Admin Interface**: Django admin for superuser management

## Technology Stack

- **Backend**: Django 5.2.5 with Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT using djangorestframework-simplejwt
- **API Documentation**: Swagger using drf-yasg
- **Admin Panel**: Django Admin

## Setup Instructions

### 1. Clone and Setup Virtual Environment

```bash
cd /path/to/project
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy the environment example file and configure your settings:

```bash
cp env_example.txt .env
```

Edit `.env` with your actual values:
- Set `SECRET_KEY` to a secure random string
- Configure PostgreSQL database credentials
- Set `DEBUG=False` for production

### 4. Database Setup

Make sure PostgreSQL is installed and running, then create the database:

```sql
-- Connect to PostgreSQL as superuser
CREATE DATABASE agnovat_db;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE agnovat_db TO postgres;
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Start Development Server

```bash
python manage.py runserver
```

## API Endpoints

### Authentication

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (returns JWT tokens)
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update user profile
- `POST /api/auth/change-password/` - Change password

### Documentation

- `/swagger/` - Swagger UI for API documentation
- `/redoc/` - ReDoc API documentation
- `/admin/` - Django admin interface

## User Roles

1. **Admin**: Full system control and access
2. **Support Worker**: Logs shifts, uploads documents, reports incidents
3. **Coordinator**: Oversees onboarding, shift approvals, incident reviews
4. **Behaviour Practitioner**: Reviews behavioral data and generates insights

## Testing the API

### 1. Register a new user:

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testworker",
    "email": "worker@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "Test",
    "last_name": "Worker",
    "role": "worker"
  }'
```

### 2. Login to get JWT tokens:

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testworker",
    "password": "testpass123"
  }'
```

### 3. Access protected profile endpoint:

```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Project Structure

```
ndis-app/
├── tavonga_system/          # Django project settings
│   ├── settings.py         # Main settings file
│   ├── urls.py            # URL configuration
│   └── wsgi.py            # WSGI configuration
├── users/                  # Custom user model app
│   ├── models.py          # User model with roles
│   ├── admin.py           # User admin configuration
│   └── serializers.py     # User serializers
├── authentication/         # JWT authentication app
│   ├── views.py           # Auth views and endpoints
│   └── urls.py            # Auth URL patterns
├── requirements.txt        # Python dependencies
├── env_example.txt        # Environment variables example
└── README.md              # This file
```

## Next Steps

This is the foundation setup based on the requirements. You can now extend the system by adding:

1. **Onboarding Module**: Document uploads and compliance tracking
2. **Scheduling Module**: Shift planning and availability management
3. **Incident Reporting**: Behavioral incident tracking and analysis
4. **Dashboard**: Role-based dashboards for different user types
5. **Notifications**: Email notifications for compliance and alerts

## Development

For development, make sure to:

1. Keep `DEBUG=True` in your `.env` file
2. Use SQLite for local development if preferred (change database settings)
3. Run `python manage.py check` to verify configuration
4. Use the Django admin at `/admin/` to manage users and data

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Project Status

🚧 **In Development** - This is an active project under development for Agnovat's support worker management needs.

## License

This project is proprietary software for Agnovat's support worker management system.
