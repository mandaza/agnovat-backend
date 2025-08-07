# 🚀 Render Deployment Guide for Agnovat System

## Files Created for Render Deployment

✅ **render.yaml** - Render service configuration
✅ **build.sh** - Build script for Render
✅ **Updated requirements.txt** - Added production dependencies
✅ **Updated settings.py** - Production database and static files configuration

## Deploy to Render

### Method 1: Using render.yaml (Recommended)

1. **Push your code to GitHub** (if not already done)
2. **Go to Render Dashboard**: [render.com](https://render.com)
3. **Connect GitHub**: Link your GitHub account
4. **Create New Service**: Click "New" → "Blueprint"
5. **Select Repository**: Choose your `agnovat-support-system` repo
6. **Render will automatically**:
   - Read the `render.yaml` file
   - Create a PostgreSQL database
   - Set up the web service
   - Configure environment variables

### Method 2: Manual Setup

If you prefer manual setup:

1. **Create PostgreSQL Database**:
   - Go to Render Dashboard
   - Click "New" → "PostgreSQL"
   - Name: `agnovat-db`
   - Note the database URL

2. **Create Web Service**:
   - Click "New" → "Web Service"
   - Connect your GitHub repo
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn tavonga_system.wsgi:application --bind 0.0.0.0:$PORT`

3. **Set Environment Variables**:
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://... (from step 1)
   ALLOWED_HOSTS=*
   CORS_ALLOW_ALL_ORIGINS=True
   ```

## Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `DEBUG` | `False` | Disable debug mode for production |
| `SECRET_KEY` | Generate new | Django secret key (Render can auto-generate) |
| `DATABASE_URL` | From database | PostgreSQL connection string |
| `ALLOWED_HOSTS` | `*` | Allow all hosts (or specify your domain) |
| `CORS_ALLOW_ALL_ORIGINS` | `True` | Allow CORS for API access |

## After Deployment

### 1. Create Superuser
After successful deployment, create a superuser:

1. Go to Render Dashboard → Your Service → Shell
2. Run: `python manage.py createsuperuser`
3. Follow prompts to create admin user

### 2. Create Test Users
```bash
python manage.py create_test_users
```

### 3. Test Your API
Your API will be available at: `https://your-service-name.onrender.com`

**Test endpoints**:
- Swagger: `https://your-service-name.onrender.com/swagger/`
- Admin: `https://your-service-name.onrender.com/admin/`
- API: `https://your-service-name.onrender.com/api/auth/login/`

### 4. Update Email Addresses (if needed)
If test users need updating:
```bash
python manage.py shell
# Then run the email update script
```

## Troubleshooting

### Common Issues:

1. **ModuleNotFoundError: No module named 'app'**
   - ✅ Fixed: Using correct WSGI path `tavonga_system.wsgi:application`

2. **Static files not loading**
   - ✅ Fixed: Added WhiteNoise middleware and STATIC_ROOT

3. **Database connection errors**
   - Check DATABASE_URL environment variable
   - Ensure PostgreSQL database is created

4. **Build failures**
   - Check build logs in Render dashboard
   - Verify all dependencies in requirements.txt

## Production Settings

The app automatically detects production environment via `DATABASE_URL`:
- **Development**: Uses SQLite database
- **Production**: Uses PostgreSQL from Render

## Security Notes

- DEBUG is disabled in production
- SECRET_KEY should be generated fresh
- ALLOWED_HOSTS can be restricted to your domain
- Consider using environment-specific CORS settings

---

**Ready to deploy!** Push your changes and follow the steps above.
