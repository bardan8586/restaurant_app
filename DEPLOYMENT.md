# 🚀 Deployment Guide - Restaurant Reservation System

## Quick Deploy to Railway.app (Recommended)

### Step 1: Prepare Your Code
1. ✅ Your app is already configured for deployment!
2. Make sure you have a GitHub account

### Step 2: Push to GitHub
```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Restaurant reservation system ready for deployment"

# Create a new repository on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/restaurant-reservation.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Railway
1. Go to [railway.app](https://railway.app) and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your restaurant-reservation repository
4. Railway will automatically:
   - Detect it's a Python app
   - Install dependencies from requirements.txt
   - Set up a PostgreSQL database
   - Deploy your app!

### Step 4: Configure Database
Railway automatically provides a DATABASE_URL environment variable, so no manual configuration needed!

### Step 5: Share Your App!
- Railway will give you a URL like: `https://your-app-name.railway.app`
- Share this with your friends!
- Admin login: `admin` / `admin123`

## Alternative: Deploy to Render.com

1. Go to [render.com](https://render.com) and sign up
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. Add PostgreSQL database (free tier)
6. Deploy!

## Alternative: Deploy to Heroku

```bash
# Install Heroku CLI first
pip install gunicorn

# Create Procfile (already created)
echo "web: python app.py" > Procfile

# Deploy to Heroku
heroku create your-restaurant-app
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

## Environment Variables (Auto-configured)
- `DATABASE_URL` - Automatically provided by hosting platforms
- `SECRET_KEY` - Uses default for demo (change in production)
- `PORT` - Automatically set by hosting platforms

## 🎉 What Your Friends Will See
- Beautiful restaurant reservation interface
- Ability to book tables
- Admin can manage bookings at `/login`
- Real-time table availability
- Professional restaurant branding

## Admin Access
- **URL**: `your-app-url.com/login`
- **Username**: `admin`
- **Password**: `admin123`

Your app is production-ready! 🚀
