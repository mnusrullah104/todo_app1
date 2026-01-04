# Docker Setup Guide

This guide explains how to run the Todo application using Docker and Docker Compose.

## Prerequisites

- Docker (version 20.10+)
- Docker Compose (version 2.0+)

## Quick Start

### 1. Clone and Navigate

```bash
cd phase2
```

### 2. Create Environment File

Copy the example environment file and update values:

```bash
cp .env.example .env
```

**Important:** Change the `BETTER_AUTH_SECRET` to a random string (minimum 32 characters) in production:

```bash
# Generate a secure secret (Linux/Mac)
openssl rand -hex 32

# Or use Python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Start All Services

```bash
docker-compose up -d
```

This will start:
- **PostgreSQL** database on port 5432
- **FastAPI** backend on port 8000
- **Next.js** frontend on port 3000

### 4. Verify Services

Check that all services are running:

```bash
docker-compose ps
```

You should see three services with status "Up":
- `todo_db`
- `todo_backend`
- `todo_frontend`

### 5. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## Common Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Stop Services

```bash
docker-compose down
```

### Stop and Remove Volumes

```bash
docker-compose down -v
```

### Rebuild Services

```bash
# Rebuild all
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build backend
```

### Execute Commands in Containers

```bash
# Backend shell
docker-compose exec backend sh

# Run migrations
docker-compose exec backend alembic upgrade head

# Frontend shell
docker-compose exec frontend sh

# Database shell
docker-compose exec db psql -U todouser -d tododb
```

## Development Workflow

### Hot Reload

Both frontend and backend support hot reload:
- Changes to Python files will automatically restart the backend
- Changes to TypeScript/React files will trigger Next.js hot reload

### Database Migrations

```bash
# Create a new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec backend alembic upgrade head

# Rollback migration
docker-compose exec backend alembic downgrade -1
```

### Install New Dependencies

**Backend:**
```bash
# Add to requirements.txt, then:
docker-compose exec backend pip install -r requirements.txt

# Or rebuild
docker-compose up -d --build backend
```

**Frontend:**
```bash
# Add to package.json, then:
docker-compose exec frontend npm install

# Or rebuild
docker-compose up -d --build frontend
```

## Troubleshooting

### Database Connection Issues

1. Check if database is healthy:
```bash
docker-compose ps db
```

2. Verify credentials in `.env` file

3. Restart services:
```bash
docker-compose restart backend
```

### Backend Won't Start

1. Check logs:
```bash
docker-compose logs backend
```

2. Common issues:
   - Database not ready (wait for health check)
   - Migration errors (check migration files)
   - Missing dependencies (rebuild container)

### Frontend Build Errors

1. Clear Next.js cache:
```bash
docker-compose exec frontend rm -rf .next
docker-compose restart frontend
```

2. Rebuild with no cache:
```bash
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### Port Already in Use

Change ports in `.env` file:
```env
BACKEND_PORT=8001
FRONTEND_PORT=3001
POSTGRES_PORT=5433
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

## Production Deployment

For production deployment:

1. **Update Environment Variables:**
   - Set strong `BETTER_AUTH_SECRET`
   - Use production database credentials
   - Set `BACKEND_CORS_ORIGINS` to your frontend URL

2. **Use Production Dockerfile:**
   The included Dockerfiles are suitable for production. Ensure you:
   - Build without development dependencies
   - Use multi-stage builds (already configured)
   - Set appropriate resource limits

3. **Security Checklist:**
   - [ ] Change all default passwords
   - [ ] Use environment-specific `.env` files
   - [ ] Enable HTTPS (configure reverse proxy)
   - [ ] Set up database backups
   - [ ] Configure log aggregation
   - [ ] Enable monitoring (health checks)

4. **Reverse Proxy:**
   Use Nginx or Traefik in front of services:
   ```yaml
   # Add to docker-compose.yml
   nginx:
     image: nginx:alpine
     ports:
       - "80:80"
       - "443:443"
     volumes:
       - ./nginx.conf:/etc/nginx/nginx.conf:ro
     depends_on:
       - backend
       - frontend
   ```

## Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ▼
┌─────────────┐         ┌──────────────┐
│  Frontend   │────────▶│   Backend    │
│ (Next.js)   │         │  (FastAPI)   │
│  Port 3000  │         │  Port 8000   │
└─────────────┘         └──────┬───────┘
                               │
                               ▼
                        ┌──────────────┐
                        │  PostgreSQL  │
                        │  Port 5432   │
                        └──────────────┘
```

## Data Persistence

- **PostgreSQL data:** Stored in Docker volume `postgres_data`
- **Backup volume:**
  ```bash
  docker run --rm -v postgres_data:/data -v $(pwd):/backup \
    alpine tar czf /backup/postgres-backup.tar.gz /data
  ```

- **Restore volume:**
  ```bash
  docker run --rm -v postgres_data:/data -v $(pwd):/backup \
    alpine sh -c "cd /data && tar xzf /backup/postgres-backup.tar.gz --strip 1"
  ```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Docker Deployment](https://fastapi.tiangolo.com/deployment/docker/)
- [Next.js Docker Deployment](https://nextjs.org/docs/deployment#docker-image)
