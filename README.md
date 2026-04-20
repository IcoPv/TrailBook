# TrailBook

TrailBook is a community platform built for off-road and overland travellers. Whether you ride motorcycles, drive 4x4s, or cycle remote trails, TrailBook gives you a place to document your adventures and share them with a like-minded community.

Users can log detailed trip reports — complete with GPS waypoints, elevation data, difficulty ratings, and photo galleries — and leave trail notes on each other's routes to share real-world conditions, warnings, and tips. Trips can be tagged, searched, filtered by vehicle type and difficulty, and saved to a personal bookmark list for future reference.

Behind the scenes, photo thumbnails are generated asynchronously using Celery so uploads stay fast, and a REST API exposes trip data for external use. Role-based permissions allow moderators to keep the community clean without needing admin access.

Built with Django 6, Django REST Framework, Celery, and PostgreSQL.

---

## Features

- **Trip management** — create, edit, and delete off-road trips with difficulty ratings, vehicle type, date ranges, and tags
- **Waypoints** — add GPS waypoints to trips with coordinates, elevation, categories, and arrival dates
- **Gallery** — upload photos linked to trips or specific waypoints; thumbnails are generated asynchronously via Celery
- **Trail notes** — community comments on any trip, with moderation support
- **Bookmarks** — save trips to a personal list
- **User profiles** — extend your account with bio, avatar, vehicle type, riding experience, and location
- **REST API** — read-only JSON endpoints for trips with filtering by difficulty and vehicle type
- **Role-based permissions** — Rider and Moderator groups with distinct capabilities

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 6.0, Django REST Framework 3.17 |
| Database | PostgreSQL (via psycopg2) |
| Async tasks | Celery 5.6 + Redis |
| Image processing | Pillow |
| Frontend | Bootstrap 5, django-crispy-forms, widget-tweaks |
| Filtering | django-filter |

---

## Requirements

- Python 3.11+
- PostgreSQL
- Redis (for Celery broker and result backend)

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/IcoPv/TrailBook.git
cd TrailBook
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the template and fill in your values:

```bash
cp .env.template .env
```

Open `.env` and set each variable (see [Environment Variables](#environment-variables) below).

### 5. Create the database

```bash
psql -U postgres -c "CREATE DATABASE trail_book;"
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Collect static files

```bash
python manage.py collectstatic
```

### 9. Start the development server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`.

---

## Running Celery

Celery handles asynchronous thumbnail generation for uploaded photos. You need Redis running before starting Celery.

In a separate terminal (with the virtual environment activated):

```bash
celery -A trailbook worker --loglevel=info
```

> Without Celery running, the app works normally but photo thumbnails will not be generated automatically.

---

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# PostgreSQL
DB_NAME=trail_book
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Celery / Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key — generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | Set to `True` for local development, `False` in production |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL username |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | Database host (usually `localhost`) |
| `DB_PORT` | Database port (default: `5432`) |
| `CELERY_BROKER_URL` | Redis URL used as the Celery message broker |
| `CELERY_RESULT_BACKEND` | Redis URL used to store Celery task results |

---

## Running Tests

```bash
python manage.py test
```

To run tests for a specific app:

```bash
python manage.py test accounts
python manage.py test trips
python manage.py test community
```

---

## Project Structure

```
TrailBook/
├── accounts/        # Custom user profile, registration, authentication
├── api/             # Django REST Framework — trip list and detail endpoints
├── community/       # Trail notes and bookmarks
├── gallery/         # Photo uploads and async thumbnail generation
├── trips/           # Core trip model with tags, search, and CRUD
├── waypoints/       # GPS waypoints linked to trips
├── trailbook/       # Project settings, root URLs, Celery config
├── templates/       # All HTML templates
├── static/          # Static assets (CSS, JS, images)
├── media/           # User-uploaded files (created at runtime)
├── requirements.txt
└── .env.template
```

---

## API Endpoints

The REST API is available at `/api/`.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/trips/` | List all trips (paginated, filterable) |
| GET | `/api/trips/{slug}/` | Retrieve a single trip with waypoints |

**Filter parameters for the list endpoint:**

- `?difficulty=easy` — filter by difficulty level
- `?vehicle_type=4x4` — filter by vehicle type

Example: `GET /api/trips/?difficulty=moderate&vehicle_type=motorcycle`

---

## Deployment

The live application is deployed at: http://trailbook-c6gefxfdgng4exdj.swedencentral-01.azurewebsites.net/

When deploying, ensure the following:

- `DEBUG=False` in your environment
- `ALLOWED_HOSTS` includes your domain
- A production-grade web server (e.g. Gunicorn) is used
- Static files are served via a CDN or web server (not Django)
- Redis is available for Celery

---

## License

This project was developed as part of the **Django Advanced course at SoftUni**.
