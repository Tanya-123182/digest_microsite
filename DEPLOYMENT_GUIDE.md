# 🚀 Deployment Guide - News Digest App

## 📋 **Prerequisites**
- GitHub repository: [https://github.com/Tanya-123182/digest_microsite](https://github.com/Tanya-123182/digest_microsite)
- NewsAPI key: [https://newsapi.org/register](https://newsapi.org/register)
- Gemini API key: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

---

## 🌐 **Option 1: Netlify (Free Account)**

### **Step 1: Deploy to Netlify**
1. Go to [netlify.com](https://netlify.com) and sign up/login
2. Click **"New site from Git"**
3. Connect your GitHub account
4. Select your `digest_microsite` repository
5. Set build settings:
   - **Build command**: `bash setup.sh`
   - **Publish directory**: `.`
6. Click **"Deploy site"**

### **Step 2: Set Environment Variables**
1. Go to **Site settings** → **Environment variables**
2. Add these variables (they'll be available to all scopes):
   ```
   NEWS_API_KEY=your_news_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
3. Click **"Save"**

### **Step 3: Redeploy**
- Go to **Deploys** tab
- Click **"Trigger deploy"** → **"Deploy site"**

---

## ⚡ **Option 2: Vercel (Recommended - No Scope Limits)**

### **Step 1: Deploy to Vercel**
1. Go to [vercel.com](https://vercel.com) and sign up/login
2. Click **"New Project"**
3. Import your GitHub repository
4. Vercel will auto-detect the Python project
5. Click **"Deploy"**

### **Step 2: Set Environment Variables**
1. Go to **Settings** → **Environment Variables**
2. Add your API keys:
   ```
   NEWS_API_KEY=your_news_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
3. Select **Production** and **Preview** environments
4. Click **"Save"**

### **Step 3: Redeploy**
- Go to **Deployments** tab
- Click **"Redeploy"**

---

## 🚂 **Option 3: Railway (No Scope Limits)**

### **Step 1: Deploy to Railway**
1. Go to [railway.app](https://railway.app) and sign up/login
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `digest_microsite` repository
5. Railway will auto-detect the configuration

### **Step 2: Set Environment Variables**
1. Go to **Variables** tab
2. Add your API keys:
   ```
   NEWS_API_KEY=your_news_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
3. Click **"Add"**

### **Step 3: Deploy**
- Railway will automatically deploy your app
- Your app will be available at the provided URL

---

## 🎨 **Option 4: Render (No Scope Limits)**

### **Step 1: Deploy to Render**
1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `news-digest-app`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
5. Click **"Create Web Service"**

### **Step 2: Set Environment Variables**
1. Go to **Environment** tab
2. Add your API keys:
   ```
   NEWS_API_KEY=your_news_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
3. Click **"Save Changes"**

---

## ☁️ **Option 5: Streamlit Cloud (Easiest)**

### **Step 1: Deploy to Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Configure:
   - **Repository**: `Tanya-123182/digest_microsite`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
5. Click **"Deploy!"**

### **Step 2: Set Secrets**
1. Go to **Settings** → **Secrets**
2. Add your API keys in TOML format:
   ```toml
   NEWS_API_KEY = "your_news_api_key_here"
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```
3. Click **"Save"**

---

## 🔧 **Troubleshooting**

### **Common Issues:**

1. **API Key Errors**:
   - Verify your API keys are correct
   - Check that environment variables are set properly
   - Ensure no extra spaces or quotes in the values

2. **Build Failures**:
   - Check the build logs for specific errors
   - Verify all dependencies are in `requirements.txt`
   - Ensure Python version compatibility

3. **App Not Loading**:
   - Check the deployment logs
   - Verify the start command is correct
   - Ensure the port configuration is right

### **Testing Your Deployment:**

1. **Check API Status**: Go to Settings → API Status in your app
2. **Test News Fetching**: Try fetching articles with different interests
3. **Verify Features**: Test saving articles, ratings, and analytics

---

## 📊 **Platform Comparison**

| Platform | Free Tier | Environment Variables | Ease of Use | Recommended |
|----------|-----------|----------------------|-------------|-------------|
| **Vercel** | ✅ Yes | ✅ No limits | ⭐⭐⭐⭐⭐ | **Best Choice** |
| **Railway** | ✅ Yes | ✅ No limits | ⭐⭐⭐⭐ | Great Alternative |
| **Render** | ✅ Yes | ✅ No limits | ⭐⭐⭐⭐ | Good Option |
| **Streamlit Cloud** | ✅ Yes | ✅ Secrets | ⭐⭐⭐⭐⭐ | **Easiest** |
| **Netlify** | ✅ Yes | ⚠️ Limited scopes | ⭐⭐⭐ | Works but limited |

---

## 🎯 **Recommended Deployment Order:**

1. **Streamlit Cloud** (Easiest, no scope issues)
2. **Vercel** (Best overall experience)
3. **Railway** (Good alternative)
4. **Render** (Solid option)
5. **Netlify** (Works but with limitations)

---

## 🚀 **Quick Start (Recommended)**

**Use Streamlit Cloud** - it's the easiest and most reliable for Streamlit apps:

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select your repository
4. Set main file to `streamlit_app.py`
5. Add your API keys in secrets
6. Deploy!

Your app will be live in minutes! 🎉
