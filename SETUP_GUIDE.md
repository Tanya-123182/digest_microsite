# 📰 News Digest Microsite - Setup Guide

This guide will help you set up and deploy your personalized news digest microsite.

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.8+** installed on your system
- **API Keys** for NewsAPI and Gemini API
- **Git** (optional, for version control)

### 2. Get API Keys

#### NewsAPI Key
1. Visit [https://newsapi.org/](https://newsapi.org/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Free tier includes 1,000 requests per day

#### Gemini API Key
1. Visit [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Free tier includes generous usage limits

### 3. Installation

#### Option A: Automated Setup (Recommended)
```bash
# Clone or download the project
git clone <your-repo-url>
cd news-digest-microsite

# Run automated setup
python deploy.py setup

# Edit .env file with your API keys
# Then test and start
python deploy.py test
python deploy.py start
```

#### Option B: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your API keys

# Create directories
mkdir -p data utils static/css static/js static/images

# Start the application
streamlit run app.py
```

## 🔧 Configuration

### Environment Variables (.env file)

```env
# API Keys (Required)
NEWS_API_KEY=your_news_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Application Settings (Optional)
DEBUG=True
LOG_LEVEL=INFO
DATA_DIR=./data
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### Project Structure

```
news-digest-microsite/
├── app.py                 # Main Streamlit application
├── app_enhanced.py        # Enhanced version with more features
├── requirements.txt       # Python dependencies
├── deploy.py             # Deployment script
├── netlify.toml          # Netlify configuration
├── .env                  # Environment variables (create this)
├── README.md             # Project documentation
├── SETUP_GUIDE.md        # This file
├── utils/                # Utility modules
│   ├── __init__.py
│   ├── news_api.py       # NewsAPI client
│   ├── gemini_api.py     # Gemini API client
│   └── data_manager.py   # Data management
├── data/                 # User data storage
├── static/               # Static assets
│   ├── css/
│   ├── js/
│   └── images/
└── news_digest_colab.ipynb  # Google Colab notebook
```

## 🎯 Usage

### 1. Start the Application

```bash
# Using the deployment script
python deploy.py start

# Or directly with Streamlit
streamlit run app.py
```

### 2. Access the Application

- Open your browser to `http://localhost:8501`
- The application will load with a modern dashboard interface

### 3. Configure Your Preferences

1. **Select Interests**: Choose from Technology, Business, Science, Politics, Sports, Entertainment
2. **Set Frequency**: Choose daily or weekly updates
3. **Update Preferences**: Click "Update & Fetch News" to get personalized articles

### 4. Features Available

- **📰 Personalized News Feed**: Articles based on your interests
- **🤖 AI Summaries**: Automatic article summarization
- **💾 Save Articles**: Save interesting articles for later
- **⭐ Rate Articles**: Rate articles to improve recommendations
- **📊 Analytics**: View your reading statistics
- **📤 Share Articles**: Share articles with others

## 🚀 Deployment Options

### 1. Local Development

```bash
# For development and testing
python deploy.py start
```

### 2. Google Colab

1. Upload the `news_digest_colab.ipynb` file to Google Colab
2. Set up API keys in Colab secrets
3. Run the notebook cells
4. Use ngrok for public access

### 3. Netlify Deployment

1. Push your code to GitHub
2. Connect your repository to Netlify
3. Configure build settings:
   - Build command: `pip install -r requirements.txt`
   - Publish directory: `.`
4. Set environment variables in Netlify dashboard
5. Deploy!

### 4. Streamlit Cloud

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set environment variables
5. Deploy!

## 🛠️ Troubleshooting

### Common Issues

#### 1. API Key Errors
```
Error: NEWS_API_KEY not found
```
**Solution**: Check your `.env` file and ensure API keys are set correctly.

#### 2. Import Errors
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution**: Install dependencies with `pip install -r requirements.txt`

#### 3. Port Already in Use
```
Error: Port 8501 is already in use
```
**Solution**: Change the port in `.env` file or kill the existing process.

#### 4. Rate Limiting
```
Error: Rate limit exceeded
```
**Solution**: NewsAPI free tier has limits. Consider upgrading or implementing caching.

### Debug Mode

Enable debug mode for more detailed error messages:

```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### Testing

Run the test suite to verify everything works:

```bash
python deploy.py test
```

## 📊 Monitoring and Analytics

### Application Metrics

The application tracks:
- Total articles fetched
- Categories covered
- User ratings
- Saved articles
- Reading patterns

### Data Storage

User data is stored locally in the `data/` directory:
- `user_preferences.json`: User settings and interests
- `saved_articles.json`: Saved articles
- `ratings.json`: Article ratings
- `analytics.json`: Usage analytics

### Data Export/Import

```bash
# Export your data
# Available in the Settings page of the application

# Import data
# Use the data manager utility functions
```

## 🔒 Security Considerations

### API Key Security

- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate API keys regularly
- Monitor API usage to prevent abuse

### Data Privacy

- User data is stored locally by default
- No data is sent to external servers (except APIs)
- Users can export/delete their data
- Consider GDPR compliance for production use

## 🚀 Advanced Features

### Custom Categories

Add custom news categories by modifying `NEWS_CATEGORIES` in `app.py`:

```python
NEWS_CATEGORIES = {
    'Technology': ['artificial intelligence', 'cybersecurity', ...],
    'Custom Category': ['keyword1', 'keyword2', ...],
    # Add your categories here
}
```

### Custom Summarization

Modify the summarization prompts in `utils/gemini_api.py`:

```python
def summarize_article(self, title: str, content: str, max_length: int = 200) -> str:
    prompt = f"""
    Your custom summarization prompt here...
    """
```

### Additional APIs

Integrate additional news sources by extending `utils/news_api.py`:

```python
def fetch_from_custom_source(self, query: str) -> List[Dict]:
    # Implement custom news source integration
    pass
```

## 📞 Support

### Getting Help

1. **Check the logs**: Look for error messages in the console
2. **Verify API keys**: Ensure both API keys are valid
3. **Test components**: Use `python deploy.py test`
4. **Check documentation**: Review this guide and README.md

### Common Commands

```bash
# Setup project
python deploy.py setup

# Test installation
python deploy.py test

# Start application
python deploy.py start

# Full deployment
python deploy.py deploy

# Show help
python deploy.py help
```

### Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [NewsAPI Documentation](https://newsapi.org/docs)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Netlify Documentation](https://docs.netlify.com/)

## 🎉 Success!

Once you've completed the setup, you'll have a fully functional personalized news digest microsite with:

- ✅ Modern dashboard interface
- ✅ AI-powered article summarization
- ✅ Personalized news recommendations
- ✅ Save, rate, and share functionality
- ✅ Analytics and insights
- ✅ Multiple deployment options

Happy reading! 📰✨
