# CodeMentor - Collaborative Code Review Learning Platform

A Django-based platform for learning code review skills through AI-powered feedback and community collaboration.

## Features

- Submit code snippets for review
- AI-powered code analysis using Claude
- Community peer reviews
- Gamification and skill tracking
- Learning paths based on your progress

## Tech Stack

- Django 5.1.5
- PostgreSQL 16
- Redis 7
- Celery for async tasks
- Docker & Docker Compose
- Anthropic Claude API

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed
- Anthropic API key (get one at https://console.anthropic.com/)

### Installation

1. Clone the repository
2. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your-actual-api-key
   ```

4. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

5. In a new terminal, run migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

7. Access the application at http://localhost:8000

## Development

- Access Django admin at http://localhost:8000/admin
- View logs: `docker-compose logs -f`
- Run management commands: `docker-compose exec web python manage.py <command>`
- Stop containers: `docker-compose down`

## Project Structure

```
codementor/
├── codementor/          # Main project settings
├── reviews/             # Core app for code reviews
├── users/               # User management and profiles
├── static/              # Static files (CSS, JS, images)
├── templates/           # Django templates
├── media/               # User uploaded files
├── docker-compose.yml   # Docker orchestration
├── Dockerfile           # Django container
└── requirements.txt     # Python dependencies
```

## Next Steps

We'll be building this project incrementally, adding features step by step.
