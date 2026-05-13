# Gym Booking System

[![Python](https://img.shields.io/badge/python-3.13-blue?logo=python&logoColor=white)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/FastAPI-%2300BCD1.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/) [![Uvicorn](https://img.shields.io/badge/Uvicorn-%23FF6B00.svg)](https://www.uvicorn.org/) [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](https://www.docker.com/) [![DynamoDB](https://img.shields.io/badge/DynamoDB-Amazon%20DynamoDB-yellow?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/dynamodb/) [![Jinja2](https://img.shields.io/badge/Jinja2-%23B41717.svg)](https://palletsprojects.com/p/jinja/)

Lightweight FastAPI application for booking gym sessions with DynamoDB (local) support, admin tools, QR check-in, and a simple server-rendered UI using Jinja templates.

## Features
- Web UI pages for home, schedule, sign-in/sign-up, reservations, and admin dashboard
- Booking flow with reservation, cancellation, and QR generation
- Admin check-in (manual and QR) and report generation pages
- WebSocket notifications for booking updates
- Local DynamoDB support (docker-compose) and a DynamoDB Admin UI

## Tech Stack
- Python 3.13
- FastAPI + Uvicorn
- DynamoDB (local for development) via `boto3`
- Jinja2 templates (server-side rendering)

## Prerequisites
- Python 3.11+ (3.13 recommended by Dockerfile)
- Docker & Docker Compose (optional — recommended for running DynamoDB locally)

## Quickstart — Local (venv)
1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables (optional — defaults are provided for local DynamoDB):

```powershell
$env:DYNAMODB_URL = "http://localhost:8000"
$env:AWS_ACCESS_KEY_ID = "fakeAccessKeyId"
$env:AWS_SECRET_ACCESS_KEY = "fakeSecretAccessKey"
```

4. Run the app:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The UI will be available at http://localhost:8000/ (or port forwarded if using Docker Compose).

## Quickstart — Docker (recommended for local DB)
Start the application and a local DynamoDB instance via Docker Compose:

```bash
docker compose up --build
```

This will expose the app on port `8080` (proxied to FastAPI `8000`) and DynamoDB local on `8000`. DynamoDB Admin UI is available on `8001`.

Files: [docker-compose.yml](docker-compose.yml) and [Dockerfile](Dockerfile)

## Environment Variables
- `DYNAMODB_URL` — DynamoDB endpoint (default: `http://localhost:8000`)
- `AWS_ACCESS_KEY_ID` — AWS key (defaults provided for local)
- `AWS_SECRET_ACCESS_KEY` — AWS secret (defaults provided for local)

These are read by [Model/database_service.py](Model/database_service.py).

## Project Structure (high level)
- `main.py` — application entry, mounts static files and applies DB migration at startup
- `Model/` — DynamoDB models and DB service (`database_service.py`, `booking.py`, `sessions.py`, etc.)
- `Patterns/` — design-pattern organized code (Factory, Observer, Command, Decorator) used by the app
- `Service/` — business logic services (booking, user, home, gym dates)
- `Template/` — Jinja2 templates for UI pages
- `static/` — static assets, manifest, and service worker
- `View/router.py` — FastAPI router for all UI routes and admin endpoints

See code for more details in each directory.

## Important Implementation Notes
- On startup `main.py` runs a migration using `Model/database_service.DatabaseRegistryManager` which will create the following DynamoDB tables if missing: `Users`, `Sessions`, `GymAvailability`, `Bookings`.
- The app uses cookie-based simple authentication; see `Patterns/Factory/authFactory.py` and `Patterns/Service/user_service.py` for auth flows.
- Admin-only pages perform role checks and redirect non-admins to `/`.

## Usage
- Visit `/` for the home page. Other important routes implemented in [View/router.py](View/router.py):
	- `/schedule` — view upcoming dates and booking UI
	- `/reserveslot/{session_id}` — reserve a slot (POST)
	- `/cancelreservation/{booking_id}` — cancel reservation (POST)
	- `/auth/{mode}` — authentication actions (`signin`, `signup`, `signout`)
	- `/admin-dashboard`, `/qr-code-scanner`, `/report-generation` — admin pages

WebSocket updates are available at `/ws/booking-updates/{booking_id}`.

## Running Quick Checks
- There are helper scripts under `scripts/` such as `scripts/test_db.py` to exercise DB connectivity — run them inside your venv.

## Contributing
- Suggestions and pull requests welcome. Keep changes focused and add tests when possible.


---

