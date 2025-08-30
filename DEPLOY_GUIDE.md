# 🚀 Restaurant Reservation System - Deployment Guide

## Quick Deploy to Render.com (24/7 Live URL)

### **Method 1: One-Click Deploy (Recommended)**

1. **Create Render Account**: Go to [render.com](https://render.com) and sign up (free)

2. **Connect GitHub**: 
   - Upload your project to GitHub (or create a new repo)
   - Connect your GitHub account to Render

3. **Deploy with Blueprint**:
   - In Render dashboard, click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and deploy everything

4. **Get Your Live URL**: 
   - After deployment (5-10 minutes), you'll get a URL like:
   - `https://restaurant-reservation-system.onrender.com`

### **Method 2: Manual Deploy**

1. **Create Web Service**:
   - New → Web Service
   - Connect GitHub repo
   - Build Command: `./build.sh`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

2. **Create Database**:
   - New → PostgreSQL
   - Name: `restaurant-db`
   - Copy connection string

3. **Environment Variables**:
   - `DATABASE_URL`: (paste PostgreSQL connection string)
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: (generate random string)

## 🎯 Your Live App Features

✅ **24/7 Availability**: Never goes offline  
✅ **HTTPS**: Secure connections  
✅ **Auto-scaling**: Handles traffic spikes  
✅ **PostgreSQL**: Production database  
✅ **Admin Dashboard**: Full management interface  
✅ **Customer Portal**: Online reservations  

## 🔗 Share Your Live URL

Once deployed, share your restaurant system:
- **Customer Portal**: `https://your-app.onrender.com`
- **Admin Dashboard**: `https://your-app.onrender.com/login`
- **API Endpoints**: `https://your-app.onrender.com/api/stats`

## ⚡ Quick Tips

- **First load**: May take 30 seconds (free tier limitation)
- **Database**: PostgreSQL provides 1GB free storage
- **Updates**: Auto-deploys when you push to GitHub
- **Monitoring**: Built-in metrics and logs available
