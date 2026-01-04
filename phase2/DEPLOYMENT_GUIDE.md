# Deployment Guide

This guide covers deploying the Todo Web Application to various platforms.

## Table of Contents

- [Railway Deployment](#railway-deployment)
- [Vercel Deployment (Frontend)](#vercel-deployment-frontend)
- [Render Deployment](#render-deployment)
- [Docker Deployment](#docker-deployment)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Post-Deployment](#post-deployment)

---

## Railway Deployment

Railway provides an easy way to deploy both backend and database.

### Prerequisites

- Railway account ([railway.app](https://railway.app))
- Railway CLI (optional): `npm i -g @railway/cli`

### Step 1: Create New Project

```bash
# Login to Railway
railway login

# Create new project
railway init
```

### Step 2: Add PostgreSQL Database

1. Go to your Railway project dashboard
2. Click "+ New" → "Database" → "PostgreSQL"
3. Railway will automatically create a PostgreSQL instance

### Step 3: Deploy Backend

1. In Railway dashboard, click "+ New" → "GitHub Repo"
2. Select your repository and choose `phase2/backend` as root directory
3. Railway will auto-detect the Python app

**Configure Environment Variables:**

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
BETTER_AUTH_SECRET=your-super-secret-jwt-key-min-32-chars
BACKEND_CORS_ORIGINS=https://your-frontend-domain.vercel.app
PORT=8000
```

**Configure Build:**
- Build Command: `pip install -r requirements.txt`
- Start Command: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 4: Run Migrations

```bash
# Using Railway CLI
railway run alembic upgrade head

# Or via web dashboard
# Go to Settings → Deploy → add migration command
```

### Step 5: Get Backend URL

Your backend will be available at: `https://your-app-name.up.railway.app`

---

## Vercel Deployment (Frontend)

Vercel is perfect for Next.js applications.

### Prerequisites

- Vercel account ([vercel.com](https://vercel.com))
- Vercel CLI (optional): `npm i -g vercel`

### Step 1: Prepare Frontend

Ensure `next.config.js` has output configuration:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone', // For Docker
}

module.exports = nextConfig
```

### Step 2: Deploy via Git

1. Push code to GitHub
2. Go to [vercel.com/new](https://vercel.com/new)
3. Import your repository
4. Set **Root Directory** to `phase2/frontend`
5. Configure environment variables (see below)
6. Click "Deploy"

### Step 3: Configure Environment Variables

```env
NEXT_PUBLIC_API_BASE_URL=https://your-backend-domain.up.railway.app
```

### Step 4: Deploy via CLI (Alternative)

```bash
cd phase2/frontend
vercel --prod
```

---

## Render Deployment

Render is another great option for full-stack apps.

### Deploy PostgreSQL

1. Go to [render.com/new/database](https://dashboard.render.com/new/database)
2. Create a PostgreSQL instance
3. Note the Internal Database URL

### Deploy Backend

1. Go to [render.com/new/web](https://dashboard.render.com/new/web)
2. Connect your GitHub repository
3. Configure:
   - **Name**: todo-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd phase2/backend && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**: (see below)

```env
DATABASE_URL=<your-postgres-internal-url>
BETTER_AUTH_SECRET=your-super-secret-key
BACKEND_CORS_ORIGINS=https://your-frontend.onrender.com
PYTHON_VERSION=3.11
```

### Deploy Frontend

1. Create new Static Site
2. Configure:
   - **Build Command**: `cd phase2/frontend && npm install && npm run build`
   - **Publish Directory**: `phase2/frontend/out`
   - **Environment Variables**:
     ```env
     NEXT_PUBLIC_API_BASE_URL=https://your-backend.onrender.com
     ```

---

## Docker Deployment

For self-hosting or cloud providers (AWS, GCP, Azure).

### Prerequisites

- Docker and Docker Compose installed
- Server with SSH access
- Domain name (optional but recommended)

### Step 1: Clone Repository

```bash
ssh user@your-server
git clone https://github.com/your-username/todo-app.git
cd todo-app/phase2
```

### Step 2: Configure Environment

```bash
cp .env.example .env
nano .env
```

Update values:
```env
POSTGRES_USER=todouser
POSTGRES_PASSWORD=<strong-password>
POSTGRES_DB=tododb

BETTER_AUTH_SECRET=<generate-secure-random-string>
BACKEND_CORS_ORIGINS=https://yourdomain.com
```

### Step 3: Build and Run

```bash
docker-compose up -d
```

### Step 4: Configure Reverse Proxy (Nginx)

```nginx
# /etc/nginx/sites-available/todo-app

server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket support (if needed)
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/todo-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: Enable HTTPS with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## Environment Variables

### Backend Environment Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` | Yes |
| `BETTER_AUTH_SECRET` | JWT signing key (min 32 chars) | `your-secret-key-here` | Yes |
| `BACKEND_CORS_ORIGINS` | Allowed frontend origins | `https://app.com,https://www.app.com` | Yes |
| `PORT` | Server port | `8000` | No |

**Generating Secure Secret:**
```bash
# Linux/Mac
openssl rand -hex 32

# Python
python -c "import secrets; print(secrets.token_hex(32))"

# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

### Frontend Environment Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `NEXT_PUBLIC_API_BASE_URL` | Backend API URL | `https://api.yourdomain.com` | Yes |

---

## Database Setup

### Run Migrations

After deploying the backend:

```bash
# Railway
railway run alembic upgrade head

# Render
# Add to build command: alembic upgrade head &&

# Docker
docker-compose exec backend alembic upgrade head

# Manual
cd backend
python -m alembic upgrade head
```

### Seed Database (Optional)

For development/testing:

```bash
# Railway
railway run python -m app.scripts.seed_database

# Docker
docker-compose exec backend python -m app.scripts.seed_database

# Manual
cd backend
python -m app.scripts.seed_database
```

---

## Post-Deployment

### 1. Verify Health

```bash
curl https://your-backend-url.com/health
```

Expected response:
```json
{
  "status": "ok",
  "database": "connected"
}
```

### 2. Test Authentication

```bash
# Register user
curl -X POST https://your-backend-url.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User"
  }'

# Login
curl -X POST https://your-backend-url.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 3. Monitor Logs

**Railway:**
```bash
railway logs
```

**Render:**
Check the "Logs" tab in dashboard

**Docker:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 4. Setup Monitoring

Recommended services:
- **Uptime**: [UptimeRobot](https://uptimerobot.com/)
- **Errors**: [Sentry](https://sentry.io/)
- **Logs**: [Logtail](https://logtail.com/)
- **Analytics**: [Plausible](https://plausible.io/)

### 5. Backup Database

**Railway/Render:**
- Use platform's automated backups
- Or use `pg_dump`:
  ```bash
  pg_dump $DATABASE_URL > backup.sql
  ```

**Docker:**
```bash
docker-compose exec db pg_dump -U todouser tododb > backup.sql
```

---

## Troubleshooting

### Backend Won't Start

1. Check environment variables are set correctly
2. Verify database connection:
   ```bash
   psql $DATABASE_URL
   ```
3. Check logs for detailed errors

### CORS Errors

1. Ensure `BACKEND_CORS_ORIGINS` includes your frontend URL
2. Verify frontend is using correct backend URL
3. Check for trailing slashes in URLs

### Database Migration Errors

```bash
# Reset migrations (DANGER: deletes data)
alembic downgrade base
alembic upgrade head

# Or create new migration
alembic revision --autogenerate -m "fix"
```

### 429 Rate Limit Errors

Rate limits are per-IP:
- Registration: 5 requests / 15 minutes
- Login: 10 requests / 15 minutes

For testing, temporarily disable in `app/middleware/rate_limit.py`

---

## Security Checklist

Before going to production:

- [ ] Change `BETTER_AUTH_SECRET` to a strong random value
- [ ] Use HTTPS (SSL/TLS certificates)
- [ ] Enable database backups
- [ ] Set strong database passwords
- [ ] Configure firewall rules
- [ ] Enable rate limiting
- [ ] Setup monitoring and alerts
- [ ] Review CORS origins
- [ ] Enable security headers
- [ ] Use environment-specific configs
- [ ] Setup error tracking (Sentry)
- [ ] Configure log rotation
- [ ] Test disaster recovery

---

## Performance Optimization

### Database

```sql
-- Create indexes
CREATE INDEX idx_tasks_user_id_created ON tasks(user_id, created_at DESC);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

### Backend

- Enable caching (Redis)
- Use connection pooling
- Enable gzip compression
- Set appropriate worker count

### Frontend

- Enable Next.js Image Optimization
- Use CDN for static assets
- Enable ISR (Incremental Static Regeneration)
- Minimize bundle size

---

## Cost Estimates

### Free Tier Options

| Platform | Backend | Database | Frontend | Total |
|----------|---------|----------|----------|-------|
| Railway | Free trial | $5/mo | - | $5/mo |
| Vercel + Railway | $5/mo | $5/mo | Free | $10/mo |
| Render | Free | Free | Free | $0 |

### Production Options

| Platform | Backend | Database | Frontend | Total |
|----------|---------|----------|----------|-------|
| Railway Pro | $20/mo | $10/mo | - | $30/mo |
| Vercel + AWS RDS | $20/mo | $30/mo | $20/mo | $70/mo |
| Self-hosted VPS | $5/mo | included | included | $5/mo |

---

## Support

For issues or questions:
- Open an issue on GitHub
- Email: support@todoapp.example.com
- Documentation: https://docs.todoapp.example.com

---

**Last Updated:** 2026-01-04
**Version:** 1.0.0
