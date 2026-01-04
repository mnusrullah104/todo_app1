# 🚀 Quick Start: Deploy to Vercel in 10 Minutes

This is the fastest way to get your Todo app live on the internet.

## ✅ What You Need

- GitHub account
- Vercel account ([vercel.com](https://vercel.com) - sign up with GitHub)
- Railway account ([railway.app](https://railway.app) - sign up with GitHub)

---

## 📋 Step-by-Step Instructions

### Part 1: Backend (Railway) - 5 minutes

1. **Push code to GitHub** (if not already done)
   ```bash
   git push origin 002-fullstack-todo-web
   ```

2. **Go to Railway:** https://railway.app/dashboard

3. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - **Set Root Directory:** `phase2/backend`

4. **Add PostgreSQL Database**
   - In your project, click "+ New"
   - Select "Database" → "PostgreSQL"
   - Done! (Railway auto-configures connection)

5. **Set Environment Variables**

   Click your backend service → Variables tab → Add:

   ```
   DATABASE_URL = ${{Postgres.DATABASE_URL}}
   BETTER_AUTH_SECRET = <paste-random-string>
   BACKEND_CORS_ORIGINS = https://*.vercel.app
   PORT = 8000
   PYTHON_VERSION = 3.11
   ```

   **Generate BETTER_AUTH_SECRET:** (pick one)
   ```bash
   # Windows (PowerShell)
   [Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))

   # Mac/Linux
   openssl rand -hex 32

   # Python (any OS)
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

6. **Configure Build Command**

   Settings → Deploy:
   - **Start Command:** `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

7. **Deploy!**
   - Railway auto-deploys on push
   - Wait 2-3 minutes
   - Copy your Railway URL (looks like: `https://xxx.up.railway.app`)

8. **Test Backend**
   ```bash
   curl https://your-railway-url.up.railway.app/health
   ```

   Should return: `{"status":"ok","database":"connected"}`

---

### Part 2: Frontend (Vercel) - 5 minutes

1. **Go to Vercel:** https://vercel.com/new

2. **Import Git Repository**
   - Click "Import Project"
   - Select your GitHub repository
   - Click "Import"

3. **Configure Project**
   - **Framework Preset:** Next.js (auto-detected)
   - **Root Directory:** Click "Edit" → Enter `phase2/frontend`
   - **Build Command:** `npm run build` (default)
   - **Output Directory:** `.next` (default)

4. **Add Environment Variable**

   Click "Environment Variables":

   | Name | Value |
   |------|-------|
   | `NEXT_PUBLIC_API_BASE_URL` | `https://your-railway-url.up.railway.app` |

   ⚠️ Replace with your actual Railway URL from Step 1.7

5. **Deploy!**
   - Click "Deploy"
   - Wait 1-2 minutes
   - Vercel gives you a URL like: `https://your-app.vercel.app`

6. **Update Backend CORS**

   Go back to Railway → Backend → Variables:

   Update `BACKEND_CORS_ORIGINS`:
   ```
   https://your-app.vercel.app,https://*.vercel.app
   ```

   ⚠️ Replace `your-app` with your actual Vercel subdomain

   Backend will auto-redeploy.

---

## 🎉 You're Live!

Open your Vercel URL: `https://your-app.vercel.app`

1. Click "Register" → Create account
2. Login → Create a task
3. ✅ You have a live full-stack app!

---

## 📸 Quick Visual Guide

### Railway Setup

```
1. New Project → GitHub Repo → [your-repo]
2. Root Directory: phase2/backend
3. + New → Database → PostgreSQL
4. Variables → Add environment variables (see above)
5. Settings → Deploy → Set start command
```

### Vercel Setup

```
1. New Project → Import from Git → [your-repo]
2. Root Directory: phase2/frontend
3. Environment Variables → Add API URL
4. Deploy
5. Update Railway CORS
```

---

## 🐛 Troubleshooting

### "Failed to fetch" error on frontend

**Fix:**
1. Check Railway backend is running (green dot)
2. Verify API URL in Vercel environment variables
3. Check CORS in Railway includes your Vercel domain
4. Redeploy both services

### "Database connection failed"

**Fix:**
1. Check PostgreSQL is created in Railway
2. Verify `DATABASE_URL = ${{Postgres.DATABASE_URL}}` in variables
3. Both services must be in same Railway project

### Can't login after deployment

**Fix:**
1. Clear browser localStorage
2. Make sure `BETTER_AUTH_SECRET` is set
3. Try registering a new account

---

## 💰 Costs

- **Vercel:** FREE (Hobby tier - unlimited projects)
- **Railway:** $5 trial credit → ~$5/month after
- **Total:** ~$5/month

---

## 📚 Next Steps

✅ **Working app?** Great! Now:

1. **Custom Domain** (optional)
   - Vercel: Settings → Domains
   - Railway: Settings → Domains

2. **Seed Demo Data** (optional)
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli

   # Login and link
   railway login
   railway link

   # Seed database
   railway run python -m app.scripts.seed_database
   ```

   Demo accounts:
   - `demo@example.com` / `password123`
   - `john@example.com` / `password123`
   - `jane@example.com` / `password123`

3. **Monitor**
   - Vercel: Project → Analytics
   - Railway: Service → Metrics

4. **Auto-deploy** (already configured!)
   - Push to GitHub → Both deploy automatically

---

## 🆘 Need Help?

1. Check full guide: `VERCEL_DEPLOYMENT.md`
2. Check deployment guide: `DEPLOYMENT_GUIDE.md`
3. Open GitHub issue

---

**Estimated Time:** 10 minutes
**Difficulty:** Easy
**Requirements:** GitHub account + 2 free signups

Happy deploying! 🎊
