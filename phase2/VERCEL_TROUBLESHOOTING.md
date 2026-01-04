# 🔧 Vercel Deployment Troubleshooting Guide

## Common 404 NOT_FOUND Error

If you're seeing `404: NOT_FOUND` on Vercel, follow these steps:

---

## ✅ Solution Steps

### Step 1: Verify Root Directory Configuration

**Problem:** Vercel is looking in the wrong directory

**Solution:**
1. Go to Vercel Dashboard → Your Project → Settings → General
2. Find "Root Directory" setting
3. **Must be:** `phase2/frontend`
4. Click "Save"
5. Redeploy from Deployments tab

### Step 2: Check Build Configuration

**Problem:** Build command or framework not detected

**Solution:**
1. Go to Settings → General
2. Verify settings:
   - **Framework Preset:** Next.js (should auto-detect)
   - **Build Command:** `npm run build` (default)
   - **Output Directory:** `.next` (default)
   - **Install Command:** `npm install` (default)

### Step 3: Verify Environment Variables

**Problem:** Missing or incorrect environment variables

**Solution:**
1. Go to Settings → Environment Variables
2. Add this variable for all environments (Production, Preview, Development):

   ```
   Name: NEXT_PUBLIC_API_BASE_URL
   Value: https://your-backend.up.railway.app
   ```

3. **Important:** Must start with `NEXT_PUBLIC_` to be available in browser
4. Replace with your actual Railway backend URL

### Step 4: Check Node.js Version

**Problem:** Incompatible Node version

**Solution:**
1. Vercel uses Node 18.x by default (compatible with our app)
2. If you need to override, add to `package.json`:
   ```json
   {
     "engines": {
       "node": ">=18.x"
     }
   }
   ```

### Step 5: Redeploy After Fixes

**Important:** Changes to settings require redeployment!

1. Go to Deployments tab
2. Click "..." on latest deployment → "Redeploy"
3. Or push a new commit to trigger auto-deploy

---

## 🐛 Other Common Issues

### Build Fails with TypeScript Errors

**Symptoms:**
- Build logs show TypeScript compilation errors
- Red X on deployment

**Solution:**
```bash
# Test build locally first
cd phase2/frontend
npm install
npm run build

# Fix any errors shown
# Common fixes:
# - Check for React.Node (should be React.ReactNode)
# - Check for missing imports
# - Check tsconfig.json settings
```

### "Module not found" Errors

**Symptoms:**
- Build fails with "Cannot find module '@/components/...'"
- Import errors

**Solution:**
1. Check `tsconfig.json` has correct paths:
   ```json
   {
     "compilerOptions": {
       "paths": {
         "@/*": ["./*"]
       }
     }
   }
   ```

2. Verify all imports use correct paths:
   ```typescript
   // Correct
   import Button from "@/components/ui/Button";

   // Wrong
   import Button from "components/ui/Button";
   ```

### Environment Variables Not Working

**Symptoms:**
- `NEXT_PUBLIC_API_BASE_URL` is undefined
- API calls fail with "undefined" URL

**Solution:**
1. Ensure variable name starts with `NEXT_PUBLIC_`
2. Redeploy after adding environment variables
3. Clear browser cache and hard refresh
4. Check browser console: `console.log(process.env.NEXT_PUBLIC_API_BASE_URL)`

### Blank Page or White Screen

**Symptoms:**
- Page loads but shows nothing
- No errors in browser console

**Solution:**
1. Check browser console for JavaScript errors
2. Verify API calls are working (Network tab)
3. Check if backend is accessible:
   ```bash
   curl https://your-backend.up.railway.app/health
   ```
4. Verify CORS is configured in backend

### CORS Errors

**Symptoms:**
- "Access to fetch... has been blocked by CORS policy"
- API calls fail in browser console

**Solution:**
1. Go to Railway → Backend → Variables
2. Update `BACKEND_CORS_ORIGINS`:
   ```
   https://your-app.vercel.app,https://*.vercel.app
   ```
3. Must include your exact Vercel domain
4. Wait for Railway to redeploy
5. Clear browser cache

---

## 📊 Vercel Deployment Checklist

Before redeploying, verify:

- [ ] Root Directory is `phase2/frontend`
- [ ] Framework Preset is Next.js
- [ ] Environment variable `NEXT_PUBLIC_API_BASE_URL` is set
- [ ] Backend URL in env variable is correct (https://)
- [ ] Railway backend CORS includes Vercel domain
- [ ] No TypeScript errors locally (`npm run build`)
- [ ] All required files exist (layout.tsx, page.tsx, etc.)

---

## 🔍 How to Debug

### View Build Logs

1. Go to Vercel Dashboard → Deployments
2. Click on failed/successful deployment
3. Click "Building" section to expand
4. Read error messages carefully

### View Function Logs

1. Go to Deployment → Functions tab
2. Check for runtime errors
3. Look for helpful error messages

### Test Locally First

Always test locally before deploying:

```bash
cd phase2/frontend

# Install dependencies
npm install

# Create .env.local with backend URL
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env.local

# Build
npm run build

# Run production build
npm start

# Open http://localhost:3000
```

If it works locally, the issue is likely configuration in Vercel.

---

## 🚀 Correct Vercel Configuration

Here's what your Vercel project settings should look like:

### General Settings
```
Framework Preset: Next.js
Root Directory: phase2/frontend
Build Command: npm run build
Output Directory: .next
Install Command: npm install
Development Command: npm run dev
```

### Environment Variables
```
Name: NEXT_PUBLIC_API_BASE_URL
Value: https://your-backend-url.up.railway.app
Environments: Production, Preview, Development
```

### Build & Development Settings
```
Node.js Version: 18.x (default)
Package Manager: npm
```

---

## 📱 Quick Fixes Summary

| Error | Quick Fix |
|-------|-----------|
| 404 NOT_FOUND | Check Root Directory = `phase2/frontend` |
| Build fails | Run `npm run build` locally, fix errors |
| Blank page | Check browser console, verify API URL |
| CORS errors | Update Railway CORS with Vercel domain |
| Env vars not working | Redeploy after adding variables |
| Module not found | Check import paths use `@/` |

---

## 🆘 Still Having Issues?

### 1. Check Vercel Status
Visit: https://www.vercel-status.com/

### 2. Review Vercel Docs
- Next.js on Vercel: https://vercel.com/docs/frameworks/nextjs
- Environment Variables: https://vercel.com/docs/projects/environment-variables

### 3. Railway Backend Check
Ensure backend is working:
```bash
# Should return: {"status":"ok","database":"connected"}
curl https://your-backend.up.railway.app/health

# Should return: {"message":"Todo API - Phase II",...}
curl https://your-backend.up.railway.app/
```

### 4. Compare with Working Example
- Check your repository matches the structure
- Verify all files are committed and pushed
- Review git history for any missing commits

---

## ✅ After Fixing

1. **Redeploy** from Vercel dashboard
2. **Wait** 1-2 minutes for deployment
3. **Clear** browser cache (Ctrl+Shift+R or Cmd+Shift+R)
4. **Test** your app

If it works, you're all set! 🎉

If not, check the logs again and compare with this guide.

---

**Last Updated:** 2026-01-04
**For More Help:** Check QUICKSTART_VERCEL.md or VERCEL_DEPLOYMENT.md
