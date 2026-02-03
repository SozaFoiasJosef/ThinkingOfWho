# ThinkingOfWhoe Production Deployment Guide

## Production Checklist

### 1. Environment Setup

Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

Edit `.env` and set:
- Generate a new `DJANGO_SECRET_KEY` (use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- Set `DJANGO_DEBUG=False`
- Add your domain to `DJANGO_ALLOWED_HOSTS`
- Configure `DATABASE_URL` for PostgreSQL

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

Run migrations:
```bash
python manage.py migrate
```

Create superuser:
```bash
python manage.py createsuperuser
```

### 4. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 5. Run Production Server

Using Gunicorn:
```bash
gunicorn ThinkingOfWho.wsgi:application --bind 0.0.0.0:8000
```

## Key Changes Made

### settings.py
- ✅ `SECRET_KEY` uses environment variable
- ✅ `DEBUG` controlled by environment variable (defaults to False)
- ✅ `ALLOWED_HOSTS` configurable via environment
- ✅ PostgreSQL support with `DATABASE_URL`
- ✅ WhiteNoise for static file serving
- ✅ `STATIC_ROOT` configured for collected static files
- ✅ Security headers (HSTS, SSL redirect, secure cookies)
- ✅ XSS and clickjacking protection

### Security Features
- SSL/HTTPS enforcement in production
- Secure session and CSRF cookies
- HTTP Strict Transport Security (HSTS)
- Content type sniffing protection
- XSS filter enabled

### Static Files
- WhiteNoise middleware for efficient static file serving
- Compressed and cached static files
- Separate `STATIC_ROOT` for collected files

## Deployment Platforms

### DigitalOcean/AWS/Railway
1. Set environment variables in platform dashboard
2. Run migrations
3. Collect static files
4. Start with Gunicorn

## Notes
- Never commit `.env` file (already in .gitignore)
- Always use environment variables for sensitive data
- Test with `DEBUG=False` locally before deploying
- Ensure media files are served properly (consider cloud storage for production)
