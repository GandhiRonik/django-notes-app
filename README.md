# 📝 Django Notes App

[![Python](https://img.shields.io/badge/Python-3.9-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.1.5-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-009639?style=flat-square&logo=nginx&logoColor=white)](https://nginx.org/)
[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?style=flat-square&logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](./LICENSE)

> A full-stack note-taking web application built with a **React** frontend and a **Django REST Framework** backend, containerized with **Docker**, orchestrated via **Docker Compose**, and served through an **Nginx** reverse proxy. Includes a Jenkins-based CI/CD pipeline for automated build and deployment.

---

## Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
  - [Prerequisites](#prerequisites)
  - [Local Development (without Docker)](#local-development-without-docker)
  - [Docker Setup (Recommended)](#docker-setup-recommended)
- [Environment Variables](#-environment-variables)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Database Schema](#-database-schema)
- [Deployment Guide](#-deployment-guide)
  - [Docker Deployment](#docker-deployment)
  - [Nginx Reverse Proxy](#nginx-reverse-proxy)
  - [Jenkins CI/CD Pipeline](#jenkins-cicd-pipeline)
- [Development Workflow](#-development-workflow)
- [Coding Standards & Best Practices](#-coding-standards--best-practices)
- [Testing Instructions](#-testing-instructions)
- [Troubleshooting Guide](#-troubleshooting-guide)
- [Security Considerations](#-security-considerations)
- [Future Enhancements / Roadmap](#-future-enhancements--roadmap)
- [Contribution Guidelines](#-contribution-guidelines)
- [License](#-license)

---

## 📌 Project Overview

**Django Notes App** is a lightweight, production-ready web application that allows users to create, view, update, and delete personal notes. The project demonstrates a modern full-stack architecture:

- **Frontend:** A React single-page application (SPA) that communicates with the backend over HTTP via REST API calls.
- **Backend:** A Django REST Framework API that handles business logic and persists data to a MySQL database.
- **Infrastructure:** Docker Compose orchestrates all services (app, database, nginx) into a single deployable stack. A Jenkins pipeline automates the build → push → deploy workflow.

This project is commonly used as a **DevOps training application** for practicing Docker, Jenkins CI/CD, Nginx configuration, and containerized Python application deployment.

---

## ✨ Features

- **Note CRUD Operations** — Create, read, update, and delete notes through a clean REST API.
- **React SPA Frontend** — A pre-built React interface served as static files through Django's `whitenoise` middleware.
- **Django REST Framework** — Fully serialized JSON API with browsable API support.
- **CORS Support** — `django-cors-headers` configured for cross-origin API access from the React frontend.
- **MySQL Database** — Production-grade relational database with persistent Docker volume.
- **Gunicorn WSGI Server** — Production-ready Python application server replacing Django's development server in production.
- **Nginx Reverse Proxy** — HTTP server sitting in front of Gunicorn to handle static files, load balancing, and SSL termination.
- **Docker & Docker Compose** — Fully containerized multi-service deployment.
- **Automated CI/CD** — Jenkins pipeline with shared library functions for clone → build → push → deploy.
- **Health Checks** — Docker Compose service health checks for both the Django app and MySQL database.

---

## 🛠️ Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| Frontend | React | 18.x | Single-page application UI |
| Frontend | CSS | — | Styling |
| Backend | Python | 3.9 | Runtime |
| Backend | Django | 4.1.5 | Web framework |
| Backend | Django REST Framework | 3.14.0 | REST API layer |
| Backend | django-cors-headers | 3.13.0 | CORS policy management |
| Backend | Gunicorn | 20.1.0 | WSGI HTTP server |
| Backend | whitenoise | 6.3.0 | Static file serving |
| Database | MySQL | 8.x | Relational data storage |
| ORM | Django ORM | — | Database abstraction layer |
| Containerization | Docker | — | Application containerization |
| Orchestration | Docker Compose | — | Multi-container management |
| Reverse Proxy | Nginx | — | HTTP proxy & static serving |
| CI/CD | Jenkins | — | Automated pipeline |
| Registry | DockerHub | — | Container image registry |

---

## 🏗️ System Architecture

```
                         ┌─────────────────────────────────────────┐
                         │            Docker Network                │
                         │           (notes-app-nw)                 │
                         │                                          │
  Client Browser  ──────►│  ┌─────────────┐    ┌────────────────┐  │
  (HTTP :80)             │  │    Nginx     │    │  Django App    │  │
                         │  │  (nginx_cont)│───►│  (django_cont) │  │
                         │  │   Port: 80  │    │  Port: 8000    │  │
                         │  └─────────────┘    │   Gunicorn     │  │
                         │                     └───────┬────────┘  │
                         │                             │           │
                         │                     ┌───────▼────────┐  │
                         │                     │   MySQL DB     │  │
                         │                     │   (db_cont)    │  │
                         │                     │   Port: 3306   │  │
                         │                     └────────────────┘  │
                         └─────────────────────────────────────────┘

  CI/CD Flow:
  GitHub Repo ──► Jenkins ──► docker build ──► DockerHub ──► docker-compose up
```

**Request Flow:**
1. Browser sends HTTP request to Nginx (port 80).
2. Nginx proxies API requests (`/api/*`) to Gunicorn (port 8000).
3. Gunicorn hands off requests to Django's WSGI application.
4. Django ORM queries/writes to MySQL.
5. Response returns through the same chain.

Static assets (the React build) are served either by Nginx directly or by Django via `whitenoise`.

---

## 📁 Project Structure

```
django-notes-app/
│
├── api/                          # Django REST API application
│   ├── __init__.py
│   ├── admin.py                  # Django admin registration
│   ├── apps.py                   # App configuration
│   ├── models.py                 # Note data model definition
│   ├── serializers.py            # DRF serializers (model → JSON)
│   ├── urls.py                   # API URL routing
│   └── views.py                  # API view logic (CRUD handlers)
│
├── mynotes/                      # React frontend source & build
│   ├── build/                    # Production React build (served as static)
│   │   ├── index.html
│   │   └── static/
│   └── src/                      # React source code
│       ├── App.js
│       ├── components/
│       └── index.js
│
├── nginx/                        # Nginx configuration
│   └── nginx.conf                # Reverse proxy config
│
├── notesapp/                     # Django project configuration
│   ├── __init__.py
│   ├── asgi.py                   # ASGI entry point
│   ├── settings.py               # Django settings (DB, CORS, apps)
│   ├── urls.py                   # Root URL configuration
│   └── wsgi.py                   # WSGI entry point (used by Gunicorn)
│
├── staticfiles/                  # Collected Django static files
│
├── .env                          # Environment variables (DB credentials)
├── .gitignore                    # Git ignore rules
├── db.sqlite3                    # SQLite DB (development fallback)
├── docker-compose.yml            # Multi-service container orchestration
├── Dockerfile                    # Django app container build instructions
├── Jenkinsfile                   # Jenkins declarative pipeline definition
├── manage.py                     # Django management CLI entry point
├── Procfile                      # Heroku/process runner configuration
├── requirements.txt              # Python package dependencies
└── README.md                     # Project documentation
```

### Key File Descriptions

| File / Directory | Description |
|---|---|
| `api/models.py` | Defines the `Note` model with fields like `id`, `body`, `updated`, `created` |
| `api/serializers.py` | Converts `Note` model instances to/from JSON for the API |
| `api/views.py` | Contains API view functions/classes for list, detail, create, update, delete |
| `api/urls.py` | URL patterns for the `/api/notes/` endpoints |
| `notesapp/settings.py` | Central Django config: installed apps, database (MySQL via env vars), CORS, static files, whitenoise |
| `docker-compose.yml` | Declares three services: `nginx`, `django_app`, `db` with health checks and a shared network |
| `Dockerfile` | Multi-step build: Python 3.9 base, install `mysqlclient` + pip requirements, copy source, expose 8000 |
| `Jenkinsfile` | 4-stage pipeline: Code Clone → Docker Build → Push to DockerHub → Deploy |
| `nginx/nginx.conf` | Nginx upstream pointing to `django_cont:8000`, proxying all requests |

---

## 🚀 Installation & Setup

### Prerequisites

Ensure the following are installed on your system:

| Tool | Version | Install Guide |
|---|---|---|
| Python | 3.9+ | [python.org](https://www.python.org/downloads/) |
| Node.js | 16+ | [nodejs.org](https://nodejs.org/) |
| Docker | 20.10+ | [docs.docker.com](https://docs.docker.com/get-docker/) |
| Docker Compose | 2.x | [docs.docker.com/compose](https://docs.docker.com/compose/install/) |
| Git | Any | [git-scm.com](https://git-scm.com/) |

---

### Local Development (without Docker)

**1. Clone the repository**
```bash
git clone https://github.com/GandhiRonik/django-notes-app.git
cd django-notes-app
```

**2. Create and activate a Python virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows
```

**3. Install Python dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Copy the sample env file and populate your local database credentials:
```bash
cp .env .env.local
```

Edit `.env` with your local MySQL or use SQLite (see [Environment Variables](#-environment-variables)).

**5. Apply database migrations**
```bash
python manage.py migrate
```

**6. Run the development server**
```bash
python manage.py runserver 0.0.0.0:8000
```

The API will be available at `http://localhost:8000`.

**7. (Optional) Build and serve the React frontend**
```bash
cd mynotes
npm install
npm run build
cd ..
```

The built files are placed in `mynotes/build/` and served by Django via whitenoise.

---

### Docker Setup (Recommended)

This is the standard and recommended way to run the full stack.

**1. Clone the repository**
```bash
git clone https://github.com/GandhiRonik/django-notes-app.git
cd django-notes-app
```

**2. Verify your `.env` file** (see [Environment Variables](#-environment-variables))

```bash
cat .env
```

**3. Build the Docker image**
```bash
docker build -t notes-app .
```

**4. Run with Docker Compose (full stack: app + MySQL + Nginx)**
```bash
docker-compose up -d
```

This starts:
- `db_cont` — MySQL 8 container with a persistent volume at `./data/mysql/db`
- `django_cont` — Django app with Gunicorn, waits for DB health check, runs migrations automatically
- `nginx_cont` — Nginx reverse proxy, depends on `django_cont` being healthy

**5. Verify all containers are running**
```bash
docker-compose ps
docker-compose logs -f
```

**6. Access the application**

| Service | URL |
|---|---|
| Web Application | `http://localhost` (via Nginx on port 80) |
| Django API | `http://localhost:8000/api/notes/` |
| Django Admin | `http://localhost:8000/admin/` |

**7. Tear down**
```bash
docker-compose down          # Stop containers
docker-compose down -v       # Stop and remove volumes (deletes DB data)
```

---

## 🔐 Environment Variables

The application reads database credentials from a `.env` file in the project root. **Never commit real credentials to version control.**

| Variable | Description | Default (Docker) |
|---|---|---|
| `DB_NAME` | MySQL database name | `test_db` |
| `DB_USER` | MySQL username | `root` |
| `DB_PASSWORD` | MySQL password | `root` |
| `DB_PORT` | MySQL port | `3306` |
| `DB_HOST` | MySQL hostname (container name in Docker) | `db_cont` |

**Example `.env` for Docker Compose:**
```env
DB_NAME=test_db
DB_USER=root
DB_PASSWORD=root
DB_PORT=3306
DB_HOST=db_cont
```

**Example `.env` for local development with local MySQL:**
```env
DB_NAME=notes_db
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_PORT=3306
DB_HOST=localhost
```

> ⚠️ **Security Note:** The default `.env` file committed in this repository contains example credentials. **Replace all default credentials before any production deployment.** See [Security Considerations](#-security-considerations).

---

## 📖 Usage Guide

**Creating a Note**

Navigate to the application homepage. Use the input field to enter note content and submit. The note is saved to the database and displayed in the list.

**Editing a Note**

Click on an existing note to open the detail/edit view. Modify the content and save. The `updated` timestamp is automatically refreshed.

**Deleting a Note**

Click the delete control on a note card. The note is permanently removed from the database.

**Using the Browsable API**

Django REST Framework provides a browser-friendly interface at `http://localhost:8000/api/notes/`. You can interact with the API directly from the browser or use tools like `curl` or Postman.

---

## 📡 API Documentation

The backend exposes a RESTful JSON API. All endpoints return and accept `application/json`.

### Base URL

```
http://<host>:8000/api/
```

---

### Endpoints

#### Get All Notes

```
GET /api/notes/
```

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "body": "My first note",
    "updated": "2024-01-15T10:30:00Z",
    "created": "2024-01-15T10:00:00Z"
  }
]
```

---

#### Get a Single Note

```
GET /api/notes/{id}/
```

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | Unique note identifier |

**Response `200 OK`:**
```json
{
  "id": 1,
  "body": "My first note",
  "updated": "2024-01-15T10:30:00Z",
  "created": "2024-01-15T10:00:00Z"
}
```

**Response `404 Not Found`:**
```json
{
  "detail": "Not found."
}
```

---

#### Create a Note

```
POST /api/notes/
```

**Request Body:**
```json
{
  "body": "This is a new note"
}
```

**Response `201 Created`:**
```json
{
  "id": 2,
  "body": "This is a new note",
  "updated": "2024-01-15T11:00:00Z",
  "created": "2024-01-15T11:00:00Z"
}
```

---

#### Update a Note

```
PUT /api/notes/{id}/
```

**Request Body:**
```json
{
  "body": "Updated note content"
}
```

**Response `200 OK`:**
```json
{
  "id": 1,
  "body": "Updated note content",
  "updated": "2024-01-15T12:00:00Z",
  "created": "2024-01-15T10:00:00Z"
}
```

---

#### Delete a Note

```
DELETE /api/notes/{id}/
```

**Response `204 No Content`** (empty body on success)

---

### Example with `curl`

```bash
# List all notes
curl -X GET http://localhost:8000/api/notes/

# Create a note
curl -X POST http://localhost:8000/api/notes/ \
  -H "Content-Type: application/json" \
  -d '{"body": "Hello from curl"}'

# Update a note
curl -X PUT http://localhost:8000/api/notes/1/ \
  -H "Content-Type: application/json" \
  -d '{"body": "Updated content"}'

# Delete a note
curl -X DELETE http://localhost:8000/api/notes/1/
```

---

## 🗄️ Database Schema

The application uses a single `api_note` table managed by Django ORM migrations.

### `api_note` Table

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique note identifier |
| `body` | TEXT | NOT NULL | Note content |
| `updated` | DATETIME | NOT NULL | Last modification timestamp (auto-updated) |
| `created` | DATETIME | NOT NULL | Creation timestamp (auto-set on insert) |

**Django Model (`api/models.py`):**

```python
from django.db import models

class Note(models.Model):
    body    = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]
```

> The `auto_now=True` on `updated` ensures the timestamp is refreshed on every `.save()` call. The `auto_now_add=True` on `created` sets it once at record creation and never modifies it again.

---

## 🚢 Deployment Guide

### Docker Deployment

The standard Docker Compose deployment covers all services. See [Docker Setup](#docker-setup-recommended) above for the full walkthrough.

**Production checklist before deploying:**

- [ ] Replace all default credentials in `.env`
- [ ] Set `DEBUG = False` in `notesapp/settings.py`
- [ ] Set `ALLOWED_HOSTS` to your domain name
- [ ] Configure a strong `SECRET_KEY`
- [ ] Enable HTTPS via Nginx with a valid TLS certificate
- [ ] Restrict MySQL port (3306) from public access

---

### Nginx Reverse Proxy

If deploying without Docker Compose, install and configure Nginx on the host:

```bash
sudo apt-get update
sudo apt install nginx
```

**Basic Nginx configuration (`/etc/nginx/sites-available/notes-app`):**

```nginx
upstream django_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass         http://django_backend;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/backend/staticfiles/;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/notes-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### Jenkins CI/CD Pipeline

The `Jenkinsfile` defines a 4-stage declarative pipeline using a shared Jenkins library (`@Library('Shared')`):

```
Code Clone → Docker Build → Push to DockerHub → Deploy
```

**Stage Breakdown:**

| Stage | Shared Library Function | Description |
|---|---|---|
| Code Clone | `clone(repoUrl, branch)` | Clones the repository on the dev-server agent |
| Code Build | `dockerbuild(imageName, tag)` | Runs `docker build` to produce the image |
| Push to DockerHub | `dockerpush(credId, imageName, tag)` | Authenticates with DockerHub and pushes the image |
| Deploy | `deploy()` | Runs `docker-compose up -d` on the target host |

**Setting up Jenkins:**

1. Install Jenkins with Docker and Docker Compose plugins.
2. Configure a **DockerHub credential** in Jenkins with ID `dockerHubCreds`.
3. Install and configure the shared Jenkins library named `Shared`.
4. Create a new Pipeline job pointing to your repository's `Jenkinsfile`.
5. Trigger a build manually or configure a webhook from GitHub.

**Agent Configuration:**

The pipeline runs on a Jenkins agent with label `dev-server`. Ensure this agent:
- Has Docker installed and the Jenkins user is in the `docker` group.
- Has network access to DockerHub.
- Has the repository's Docker Compose file available for the deploy step.

---

## 🔄 Development Workflow

**Recommended Git workflow:**

```
main (production) ◄── feature/xxx ◄── development work
```

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/add-note-tags
   ```

2. Make changes, write tests, and commit with meaningful messages:
   ```bash
   git add .
   git commit -m "feat: add tag field to Note model"
   ```

3. Push and open a Pull Request to `main`.

4. Jenkins CI builds and tests the branch automatically (if webhook configured).

5. After review and merge, Jenkins deploys to production.

**Commit Message Convention (Conventional Commits):**

```
feat:     New feature
fix:      Bug fix
docs:     Documentation change
chore:    Maintenance, dependency update
refactor: Code restructure without feature change
test:     Adding or updating tests
ci:       CI/CD pipeline changes
```

---

## 📏 Coding Standards & Best Practices

**Python / Django:**
- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines.
- Use Django's class-based views or `ModelViewSet` for DRY API code.
- Keep business logic out of views — use model methods or service layers.
- Never hardcode secrets; always use environment variables.
- Run `python manage.py check` before committing.

**JavaScript / React:**
- Use functional components with React Hooks.
- Keep components small and single-purpose.
- Use `async/await` for API calls instead of `.then()` chains.
- Store API base URL in environment config, not hardcoded.

**Docker:**
- Keep the Dockerfile minimal — only install what is needed.
- Use `.dockerignore` to exclude `node_modules`, `__pycache__`, `.env`, etc.
- Always tag images with a version, not just `latest` in production.
- Use named volumes for persistent data.

**General:**
- Keep `.env` out of version control (`.gitignore` must include `.env`).
- Document all non-obvious configuration choices with inline comments.
- Prefer `docker-compose up -d --build` during development to catch image changes.

---

## 🧪 Testing Instructions

### Backend Tests

Django's built-in test framework is used for unit and integration tests.

**Run all tests:**
```bash
python manage.py test
```

**Run tests for a specific app:**
```bash
python manage.py test api
```

**Write API tests in `api/tests.py`:**

```python
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Note

class NoteAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.note = Note.objects.create(body="Test note")

    def test_list_notes(self):
        url = reverse('notes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_note(self):
        url = reverse('notes-list')
        data = {"body": "New note"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_note(self):
        url = reverse('notes-detail', args=[self.note.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
```

**Run with coverage (install `coverage` first):**
```bash
pip install coverage
coverage run manage.py test
coverage report
coverage html   # generates htmlcov/ directory
```

### Frontend Tests

```bash
cd mynotes
npm test
```

### API Testing with Postman

Import the following base request collection:

- `GET    http://localhost:8000/api/notes/`
- `POST   http://localhost:8000/api/notes/`   → Body: `{"body": "test"}`
- `GET    http://localhost:8000/api/notes/1/`
- `PUT    http://localhost:8000/api/notes/1/` → Body: `{"body": "updated"}`
- `DELETE http://localhost:8000/api/notes/1/`

---

## 🔧 Troubleshooting Guide

### Container Issues

**Problem:** `docker-compose up` fails with "connection refused" or MySQL errors.

**Solution:** MySQL takes several seconds to initialize. The `django_cont` has a `depends_on` with health check, but if it fails, wait and retry:
```bash
docker-compose restart django_app
docker-compose logs db
```

---

**Problem:** `django_cont` exits immediately after starting.

**Solution:** Check the Django container logs for migration or configuration errors:
```bash
docker-compose logs django_app
```
Common causes: incorrect `.env` values, missing `DB_HOST` pointing to container name `db_cont`.

---

**Problem:** Nginx returns `502 Bad Gateway`.

**Solution:** Gunicorn is not running or not reachable. Verify:
```bash
docker-compose ps
docker exec -it django_cont curl -f http://localhost:8000/admin
```

---

### Database Issues

**Problem:** `django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")`

**Solution:** Ensure `DB_HOST` in `.env` is set to `db_cont` (the Docker container name), not `localhost`, when running inside Docker.

---

**Problem:** Migration errors on startup.

**Solution:** Run migrations manually:
```bash
docker exec -it django_cont python manage.py migrate
```

---

### Development Issues

**Problem:** `ModuleNotFoundError: No module named 'mysqlclient'`

**Solution:** Install the required system dependency first:
```bash
sudo apt-get install default-libmysqlclient-dev
pip install mysqlclient
```

---

**Problem:** React frontend not reflecting API changes (CORS error).

**Solution:** Confirm `django-cors-headers` is configured in `settings.py`:
```python
INSTALLED_APPS = ['corsheaders', ...]
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]
CORS_ALLOW_ALL_ORIGINS = True  # Development only
```

---

**Problem:** Static files not loading (404 for `/static/` resources).

**Solution:** Run `collectstatic` and ensure `whitenoise` is in `MIDDLEWARE`:
```bash
python manage.py collectstatic --noinput
```

---

## 🔒 Security Considerations

| Risk | Current State | Recommended Mitigation |
|---|---|---|
| **Default credentials** | `.env` contains `root/root` | Use strong, randomly generated passwords; rotate regularly |
| **DEBUG mode** | May be `True` in settings | Set `DEBUG = False` in production |
| **SECRET_KEY** | May use a default or weak key | Generate a strong key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| **CORS policy** | `CORS_ALLOW_ALL_ORIGINS = True` | Restrict to known frontend domains in production |
| **ALLOWED_HOSTS** | May be `['*']` | Set to your domain: `ALLOWED_HOSTS = ['yourdomain.com']` |
| **MySQL exposed** | Port 3306 may be bound to host | In `docker-compose.yml`, remove port mapping for `db` in production |
| **No HTTPS** | Plain HTTP | Configure Nginx with TLS certificate (Let's Encrypt / Certbot) |
| **No authentication** | API is open/public | Implement Django REST Framework token or JWT authentication |
| **`.env` in repo** | Committed with defaults | Add `.env` to `.gitignore`; use secrets manager in production |
| **Gunicorn workers** | Default configuration | Tune `--workers` and `--timeout` for your load profile |

---

## 🗺️ Future Enhancements / Roadmap

- [ ] **User Authentication** — Add registration, login, and per-user note isolation using JWT or session auth.
- [ ] **Note Categories / Tags** — Allow users to organize notes with labels or folders.
- [ ] **Search Functionality** — Full-text search across note bodies.
- [ ] **Rich Text Support** — Markdown rendering or WYSIWYG editor in the React frontend.
- [ ] **Pagination** — Paginate the notes list endpoint for scalability.
- [ ] **HTTPS / TLS** — Nginx SSL termination with auto-renewing Let's Encrypt certificates.
- [ ] **GitHub Actions** — Add a GitHub Actions workflow as an alternative/supplementary CI pipeline.
- [ ] **Unit Test Coverage** — Achieve >80% backend test coverage with automated reporting.
- [ ] **Redis Caching** — Cache frequently accessed notes lists with Redis.
- [ ] **PostgreSQL Support** — Add configuration option for PostgreSQL as an alternative to MySQL.
- [ ] **Docker Multi-stage Build** — Optimize image size with a multi-stage Dockerfile.
- [ ] **Kubernetes Manifests** — Provide Helm chart or raw K8s manifests for cluster deployment.
- [ ] **Note Sharing** — Allow users to share notes via public links.

---

## 🤝 Contribution Guidelines

Contributions are welcome! Please follow these steps:

**1. Fork the repository**

Click the **Fork** button on the repository page.

**2. Clone your fork**
```bash
git clone https://github.com/YOUR_USERNAME/django-notes-app.git
cd django-notes-app
```

**3. Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

**4. Make your changes**

- Follow the [Coding Standards](#-coding-standards--best-practices).
- Add or update tests to cover your changes.
- Ensure all existing tests pass: `python manage.py test`.

**5. Commit with a clear message**
```bash
git commit -m "feat: describe what you added or fixed"
```

**6. Push to your fork**
```bash
git push origin feature/your-feature-name
```

**7. Open a Pull Request**

Go to the original repository and open a Pull Request from your branch. Fill in the PR template describing:
- What change was made and why
- How it was tested
- Any screenshots (for UI changes)

**Code Review Process:**
- All PRs require at least one review before merging.
- CI must pass (Docker build, tests).
- PRs should be focused — one feature or fix per PR.

**Reporting Bugs:**

Open a GitHub Issue with:
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Docker version, Python version)

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2024 GandhiRonik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

Built with ❤️ using Django, React, Docker & Jenkins

⭐ If this project helped you, please consider giving it a star!

</div>
