# Vercel Deployment Guide for Todo App

This guide walks you through deploying the full-stack Todo application using Vercel (frontend) and Railway (backend).

## 🎯 Architecture

```
Vercel (Frontend)     →     Railway (Backend + Database)
   Next.js 15              FastAPI + PostgreSQL
```

---

## Part 1: Deploy Backend to Railway

### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"

### Step 2: Deploy PostgreSQL Database

1. In your Railway project, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway automatically provisions a PostgreSQL database
4. Note: Database URL is available as `${{Postgres.DATABASE_URL}}`

### Step 3: Deploy Backend

1. Click "+ New" → "GitHub Repo"
2. Authorize Railway to access your repository
3. Select your repository
4. **Important**: Set Root Directory to `phase2/backend`

### Step 4: Configure Backend Environment Variables

In Railway dashboard, go to your backend service → Variables tab:

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
BETTER_AUTH_SECRET=<generate-random-32-char-string>
BACKEND_CORS_ORIGINS=https://*.vercel.app
PORT=8000
PYTHON_VERSION=3.11
```

**Generate BETTER_AUTH_SECRET:**
```bash
# Option 1: Using OpenSSL (Linux/Mac/Git Bash)
openssl rand -hex 32

# Option 2: Using Python
python -c "import secrets; print(secrets.token_hex(32))"

# Option 3: Using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

### Step 5: Configure Build Settings

Go to Settings → Deploy:

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Watch Paths:** `phase2/backend/**`

### Step 6: Deploy

1. Click "Deploy" or push to your repository
2. Wait for deployment to complete (2-3 minutes)
3. Railway will provide a public URL like: `https://your-app.up.railway.app`

### Step 7: Verify Backend

Test the health endpoint:
```bash
curl https://your-backend-url.up.railway.app/health
```

Expected response:
```json
{
  "status": "ok",
  "database": "connected"
}
```

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

### Step 2: Deploy via GitHub (Recommended)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Import Project"
3. Select your GitHub repository
4. Authorize Vercel to access your repo

### Step 3: Configure Project Settings

**Framework Preset:** Next.js

**Root Directory:** `phase2/frontend`

**Build Command:** (leave default)
```bash
npm run build
```

**Output Directory:** (leave default)
```bash
.next
```

**Install Command:** (leave default)
```bash
npm install
```

### Step 4: Configure Environment Variables

In Vercel dashboard, add environment variable:

| Name | Value | Environment |
|------|-------|-------------|
| `NEXT_PUBLIC_API_BASE_URL` | `https://your-backend.up.railway.app` | Production, Preview, Development |

**Important:** Replace `your-backend.up.railway.app` with your actual Railway backend URL.

### Step 5: Deploy

1. Click "Deploy"
2. Wait for build to complete (1-2 minutes)
3. Vercel will provide a URL like: `https://your-app.vercel.app`

### Step 6: Update Backend CORS

Go back to Railway → Backend service → Variables:

Update `BACKEND_CORS_ORIGINS` to:
```env
BACKEND_CORS_ORIGINS=https://your-app.vercel.app,https://*.vercel.app
```

**Important:** Replace `your-app.vercel.app` with your actual Vercel domain.

Redeploy backend for changes to take effect.

---

## Part 3: Deploy via CLI (Alternative)

### Deploy Backend to Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project
cd phase2/backend
railway link

# Set environment variables
railway variables set BETTER_AUTH_SECRET=your-secret-here
railway variables set BACKEND_CORS_ORIGINS=https://*.vercel.app

# Deploy
railway up
```

### Deploy Frontend to Vercel

```bash
# Navigate to frontend
cd phase2/frontend

# Login
vercel login

# Deploy (follow prompts)
vercel

# Set environment variable
vercel env add NEXT_PUBLIC_API_BASE_URL production

# When prompted, enter: https://your-backend.up.railway.app

# Deploy to production
vercel --prod
```

---

## Part 4: Post-Deployment Setup

### 1. Test Authentication

Visit your Vercel URL and test:
1. Register a new account
2. Login
3. Create a task
4. Update a task
5. Delete a task

### 2. Seed Database (Optional)

```bash
# Using Railway CLI
railway run python -m app.scripts.seed_database

# Or via Railway dashboard
# Go to Settings → Deploy → One-off Commands
# Run: python -m app.scripts.seed_database
```

This creates demo accounts:
- `demo@example.com` / `password123`
- `john@example.com` / `password123`
- `jane@example.com` / `password123`

### 3. Monitor Logs

**Railway:**
```bash
railway logs
```

**Vercel:**
```bash
vercel logs
```

### 4. Setup Custom Domain (Optional)

**Vercel:**
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

**Railway:**
1. Go to Settings → Domains
2. Add custom domain
3. Configure DNS CNAME record

---

## Environment Variables Reference

### Backend (Railway)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `BETTER_AUTH_SECRET` | JWT signing key (min 32 chars) | `abc123...` |
| `BACKEND_CORS_ORIGINS` | Allowed frontend origins | `https://app.vercel.app` |
| `PORT` | Server port | `8000` |
| `PYTHON_VERSION` | Python version | `3.11` |

### Frontend (Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | Backend API URL | `https://backend.railway.app` |

---

## Troubleshooting

### Frontend: "Failed to fetch" Error

**Cause:** Frontend can't connect to backend

**Solution:**
1. Verify `NEXT_PUBLIC_API_BASE_URL` in Vercel settings
2. Check Railway backend is running: `curl https://backend-url/health`
3. Verify CORS origins in Railway include Vercel domain
4. Redeploy both services after changing environment variables

### Backend: "Database connection failed"

**Cause:** Database not accessible

**Solution:**
1. Check `DATABASE_URL` in Railway variables
2. Verify PostgreSQL database is running
3. Check Railway logs: `railway logs`
4. Ensure database and backend are in same Railway project

### Backend: "JWT token invalid"

**Cause:** Different `BETTER_AUTH_SECRET` between deployments

**Solution:**
1. Ensure `BETTER_AUTH_SECRET` is consistent
2. Redeploy backend
3. Clear frontend localStorage and re-login

### 429 Rate Limit Errors

**Cause:** Too many login/register attempts

**Solution:**
- Wait 15 minutes (rate limit window)
- Limits: 5 register/15min, 10 login/15min per IP

### Vercel Build Fails

**Common issues:**
1. Wrong root directory (should be `phase2/frontend`)
2. Missing environment variables
3. Node version mismatch

**Check build logs:**
1. Go to Vercel dashboard → Deployments
2. Click failed deployment
3. View build logs

### Railway Deploy Fails

**Common issues:**
1. Wrong root directory (should be `phase2/backend`)
2. Missing `requirements.txt`
3. Database migration errors

**Solutions:**
1. Check Railway logs
2. Verify `requirements.txt` exists
3. Manually run migrations: `railway run alembic upgrade head`

---

## Cost Estimates

### Free Tier (Hobby Projects)

| Service | Free Tier | Limitations |
|---------|-----------|-------------|
| **Vercel** | Unlimited deployments | 100GB bandwidth/month |
| **Railway** | $5 trial credit | ~$5/month after trial |
| **Total** | ~$5/month | After trial credit |

### Paid Tier (Production)

| Service | Cost | Features |
|---------|------|----------|
| **Vercel Pro** | $20/month | Custom domains, more bandwidth |
| **Railway Pro** | ~$20/month | Guaranteed resources, backups |
| **Total** | ~$40/month | Production-ready |

---

## Production Checklist

Before going live:

- [ ] Change `BETTER_AUTH_SECRET` to strong random value
- [ ] Set `BACKEND_CORS_ORIGINS` to your actual domain
- [ ] Enable HTTPS (automatic on Vercel/Railway)
- [ ] Setup custom domains
- [ ] Configure database backups (Railway settings)
- [ ] Add monitoring (Vercel Analytics, Railway Metrics)
- [ ] Test all features thoroughly
- [ ] Setup error tracking (Sentry recommended)
- [ ] Review security headers (already configured)
- [ ] Test rate limiting
- [ ] Load test with expected traffic

---

## Maintenance

### Update Application

**Push to GitHub:**
```bash
git add .
git commit -m "Update application"
git push
```

Both Vercel and Railway will auto-deploy on push.

**Rollback:**
- **Vercel:** Go to Deployments → Click previous deployment → Promote to Production
- **Railway:** Go to Deployments → Click previous deployment → Redeploy

### Database Backup

**Manual backup:**
```bash
railway run pg_dump $DATABASE_URL > backup.sql
```

**Restore:**
```bash
railway run psql $DATABASE_URL < backup.sql
```

**Automated backups:**
- Railway Pro includes automatic daily backups
- Enable in Settings → Backups

### Monitor Performance

**Vercel Analytics:**
1. Go to Project → Analytics tab
2. View page views, response times, errors

**Railway Metrics:**
1. Go to Service → Metrics tab
2. View CPU, memory, network usage

---

## Quick Reference

### Useful Commands

```bash
# Railway
railway login
railway link
railway logs
railway run <command>
railway variables set KEY=value

# Vercel
vercel login
vercel
vercel --prod
vercel logs
vercel env add KEY production
```

### Important URLs

- **Vercel Dashboard:** https://vercel.com/dashboard
- **Railway Dashboard:** https://railway.app/dashboard
- **API Docs:** https://your-backend.railway.app/docs
- **Health Check:** https://your-backend.railway.app/health

---

## Support Resources

- **Vercel Docs:** https://vercel.com/docs
- **Railway Docs:** https://docs.railway.app
- **Next.js Docs:** https://nextjs.org/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com

---

**Deployment Time:** ~15 minutes (first time)
**Difficulty:** Beginner-friendly
**Cost:** ~$5/month (after free trial)

Good luck with your deployment! 🚀
