import streamlit as st
import requests
import google.generativeai as genai
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import time

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Page configuration
st.set_page_config(
    page_title="News Digest Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Global text color fix */
    .stMarkdown, .stText, .stDataFrame, .stSelectbox, .stMultiselect {
        color: #333333 !important;
    }
    
    /* Main header */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Category cards */
    .category-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
        color: #333333;
    }
    
    /* Article cards */
    .article-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        color: #333333;
    }
    
    /* Summary boxes */
    .summary-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        color: #333333;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        border: none;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background-color: #1565c0;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Sidebar improvements */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Text elements */
    .stMarkdown p, .stMarkdown div {
        color: #333333 !important;
    }
    
    /* Select boxes and inputs */
    .stSelectbox > div > div {
        color: #333333 !important;
    }
    
    /* Data frames */
    .stDataFrame {
        color: #333333 !important;
    }
    
    /* Better contrast for all text */
    .stMarkdown, .stText, .stDataFrame, .stSelectbox, .stMultiselect, .stTextInput {
        color: #333333 !important;
    }
    
    /* Article titles */
    .article-title {
        color: #1f77b4 !important;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    /* Article descriptions */
    .article-description {
        color: #555555 !important;
        line-height: 1.6;
    }
    
    /* Source and date */
    .article-meta {
        color: #666666 !important;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {
        'interests': [],
        'frequency': 'daily',
        'saved_articles': [],
        'ratings': {}
    }

if 'news_data' not in st.session_state:
    st.session_state.news_data = []

# News categories and interests
NEWS_CATEGORIES = {
    'Technology': ['artificial intelligence', 'cybersecurity', 'software', 'hardware', 'startups'],
    'Business': ['finance', 'economy', 'markets', 'entrepreneurship', 'corporate'],
    'Science': ['research', 'discoveries', 'health', 'environment', 'space'],
    'Politics': ['government', 'policy', 'elections', 'international relations'],
    'Sports': ['football', 'basketball', 'tennis', 'olympics', 'soccer'],
    'Entertainment': ['movies', 'music', 'celebrity', 'gaming', 'streaming']
}

def fetch_news(interests, frequency='daily'):
    """Fetch news articles based on user interests"""
    news_api_key = os.getenv('NEWS_API_KEY')
    if not news_api_key:
        st.error("News API key not found. Please set NEWS_API_KEY in your environment variables.")
        return []
    
    all_articles = []
    
    for category, keywords in NEWS_CATEGORIES.items():
        if category in interests:
            for keyword in keywords[:2]:  # Limit keywords per category
                try:
                    # Calculate date range based on frequency
                    if frequency == 'daily':
                        from_date = datetime.now() - timedelta(days=1)
                    else:  # weekly
                        from_date = datetime.now() - timedelta(days=7)
                    
                    url = f"https://newsapi.org/v2/everything"
                    params = {
                        'q': keyword,
                        'from': from_date.strftime('%Y-%m-%d'),
                        'sortBy': 'publishedAt',
                        'language': 'en',
                        'apiKey': news_api_key,
                        'pageSize': 5
                    }
                    
                    response = requests.get(url, params=params)
                    if response.status_code == 200:
                        articles = response.json().get('articles', [])
                        for article in articles:
                            article['category'] = category
                            article['keyword'] = keyword
                        all_articles.extend(articles)
                    
                    time.sleep(0.1)  # Rate limiting
                    
                except Exception as e:
                    st.warning(f"Error fetching news for {keyword}: {str(e)}")
    
    return all_articles

def summarize_article(article_text, title):
    """Summarize article using Gemini API"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Please provide a concise summary (2-3 sentences) of this news article:
        
        Title: {title}
        Content: {article_text[:1000]}...
        
        Focus on the key points and main story. Make it engaging and informative.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Summary unavailable: {str(e)}"

def categorize_articles(articles):
    """Categorize articles by user interests"""
    categorized = {}
    for article in articles:
        category = article.get('category', 'General')
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(article)
    return categorized

def save_article(article):
    """Save article to user's saved list"""
    if article not in st.session_state.user_preferences['saved_articles']:
        st.session_state.user_preferences['saved_articles'].append(article)
        st.success("Article saved!")

def rate_article(article_id, rating):
    """Rate an article"""
    st.session_state.user_preferences['ratings'][article_id] = rating

def main():
    # Header
    st.markdown('<h1 class="main-header">📰 Personalized News Digest</h1>', unsafe_allow_html=True)
    
    # Sidebar for user preferences
    with st.sidebar:
        st.header("🎯 Your Preferences")
        
        # Interest selection
        st.subheader("Select Your Interests")
        selected_interests = st.multiselect(
            "Choose news categories:",
            list(NEWS_CATEGORIES.keys()),
            default=st.session_state.user_preferences['interests']
        )
        
        # Frequency selection
        st.subheader("📅 Update Frequency")
        frequency = st.selectbox(
            "How often would you like updates?",
            ['daily', 'weekly'],
            index=0 if st.session_state.user_preferences['frequency'] == 'daily' else 1
        )
        
        # Update preferences
        if st.button("🔄 Update Preferences"):
            st.session_state.user_preferences['interests'] = selected_interests
            st.session_state.user_preferences['frequency'] = frequency
            st.session_state.news_data = fetch_news(selected_interests, frequency)
            st.success("Preferences updated! Fetching latest news...")
        
        # Saved articles count
        st.subheader("📚 Saved Articles")
        st.metric("Total Saved", len(st.session_state.user_preferences['saved_articles']))
        
        if st.button("View Saved Articles"):
            st.session_state.show_saved = True
    
    # Main content area
    if st.session_state.get('show_saved', False):
        display_saved_articles()
    else:
        display_main_dashboard()

def display_main_dashboard():
    """Display the main news dashboard"""
    
    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Articles", len(st.session_state.news_data))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        categories_count = len(set(article.get('category', 'Unknown') for article in st.session_state.news_data))
        st.metric("Categories", categories_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_rating = 0
        if st.session_state.user_preferences['ratings']:
            avg_rating = sum(st.session_state.user_preferences['ratings'].values()) / len(st.session_state.user_preferences['ratings'])
        st.metric("Avg Rating", f"{avg_rating:.1f}/5")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Last Updated", datetime.now().strftime("%H:%M"))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # News feed
    if st.session_state.news_data:
        st.header("📰 Your Personalized News Feed")
        
        # Categorize articles
        categorized_articles = categorize_articles(st.session_state.news_data)
        
        # Display articles by category
        for category, articles in categorized_articles.items():
            st.markdown(f'<div class="category-card"><h3>📂 {category}</h3></div>', unsafe_allow_html=True)
            
            for article in articles:
                display_article_card(article)
    else:
        st.info("👆 Select your interests and update preferences to see your personalized news feed!")

def display_article_card(article):
    """Display a single article card"""
    st.markdown('<div class="article-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(article.get('title', 'No title'))
        st.caption(f"📅 {article.get('publishedAt', 'Unknown date')} | 📰 {article.get('source', {}).get('name', 'Unknown source')}")
        
        # Article description
        description = article.get('description', 'No description available.')
        st.write(description[:200] + "..." if len(description) > 200 else description)
        
        # Generate and display summary
        if st.button(f"🤖 Generate Summary", key=f"summary_{article.get('url', '')}"):
            with st.spinner("Generating summary..."):
                summary = summarize_article(article.get('content', ''), article.get('title', ''))
                st.markdown(f'<div class="summary-box"><strong>AI Summary:</strong><br>{summary}</div>', unsafe_allow_html=True)
        
        # Article actions
        col_action1, col_action2, col_action3 = st.columns(3)
        
        with col_action1:
            if st.button("💾 Save", key=f"save_{article.get('url', '')}"):
                save_article(article)
        
        with col_action2:
            rating = st.selectbox("⭐ Rate", [1, 2, 3, 4, 5], key=f"rate_{article.get('url', '')}")
            if st.button("Submit Rating", key=f"submit_rate_{article.get('url', '')}"):
                rate_article(article.get('url', ''), rating)
                st.success(f"Rated {rating} stars!")
        
        with col_action3:
            if st.button("📤 Share", key=f"share_{article.get('url', '')}"):
                st.write(f"Share this article: {article.get('url', '')}")
    
    with col2:
        # Article image
        if article.get('urlToImage'):
            st.image(article.get('urlToImage'), width=150)
        else:
            st.image("https://via.placeholder.com/150x100?text=No+Image", width=150)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_saved_articles():
    """Display saved articles"""
    st.header("📚 Your Saved Articles")
    
    if not st.session_state.user_preferences['saved_articles']:
        st.info("No saved articles yet. Start reading and save interesting articles!")
        if st.button("← Back to Dashboard"):
            st.session_state.show_saved = False
        return
    
    for i, article in enumerate(st.session_state.user_preferences['saved_articles']):
        st.markdown('<div class="article-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.subheader(article.get('title', 'No title'))
            st.caption(f"📅 {article.get('publishedAt', 'Unknown date')} | 📰 {article.get('source', {}).get('name', 'Unknown source')}")
            st.write(article.get('description', 'No description available.'))
            
            if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                st.session_state.user_preferences['saved_articles'].pop(i)
                st.success("Article removed!")
                st.rerun()
        
        with col2:
            if article.get('urlToImage'):
                st.image(article.get('urlToImage'), width=100)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard"):
        st.session_state.show_saved = False

if __name__ == "__main__":
    main()
