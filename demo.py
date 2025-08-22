#!/usr/bin/env python3
"""
Demo script for News Digest Microsite
Shows the application features with sample data
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="News Digest Demo",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .demo-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .article-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Sample data
SAMPLE_ARTICLES = [
    {
        "title": "AI Breakthrough: New Model Achieves Human-Level Understanding",
        "description": "Researchers have developed a new artificial intelligence model that demonstrates unprecedented understanding of complex human language and reasoning tasks.",
        "source": {"name": "Tech News Daily"},
        "publishedAt": "2024-01-15T10:30:00Z",
        "url": "https://example.com/ai-breakthrough",
        "urlToImage": "https://via.placeholder.com/400x200?text=AI+Breakthrough",
        "category": "Technology",
        "ai_summary": "A revolutionary AI model has achieved human-level performance in language understanding and reasoning tasks, marking a significant milestone in artificial intelligence research.",
        "key_points": [
            "New AI model shows human-level understanding",
            "Breakthrough in language processing",
            "Potential applications in various industries"
        ],
        "reading_time": 3
    },
    {
        "title": "Global Markets Rally on Positive Economic Data",
        "description": "Stock markets worldwide experienced significant gains following the release of encouraging economic indicators and positive corporate earnings reports.",
        "source": {"name": "Financial Times"},
        "publishedAt": "2024-01-15T09:15:00Z",
        "url": "https://example.com/markets-rally",
        "urlToImage": "https://via.placeholder.com/400x200?text=Markets+Rally",
        "category": "Business",
        "ai_summary": "Global financial markets surged as positive economic data and strong corporate earnings boosted investor confidence across major indices.",
        "key_points": [
            "Global markets show strong gains",
            "Positive economic indicators released",
            "Corporate earnings exceed expectations"
        ],
        "reading_time": 2
    },
    {
        "title": "Scientists Discover New Species in Amazon Rainforest",
        "description": "A team of researchers has identified a previously unknown species of butterfly in the Amazon rainforest, highlighting the region's incredible biodiversity.",
        "source": {"name": "Science Daily"},
        "publishedAt": "2024-01-15T08:45:00Z",
        "url": "https://example.com/new-species",
        "urlToImage": "https://via.placeholder.com/400x200?text=New+Species",
        "category": "Science",
        "ai_summary": "Researchers discovered a new butterfly species in the Amazon rainforest, demonstrating the region's rich biodiversity and the importance of conservation efforts.",
        "key_points": [
            "New butterfly species discovered",
            "Found in Amazon rainforest",
            "Highlights biodiversity importance"
        ],
        "reading_time": 4
    },
    {
        "title": "SpaceX Successfully Launches Satellite Constellation",
        "description": "SpaceX completed another successful launch of its Starlink satellite constellation, bringing global internet coverage closer to reality.",
        "source": {"name": "Space News"},
        "publishedAt": "2024-01-15T07:30:00Z",
        "url": "https://example.com/spacex-launch",
        "urlToImage": "https://via.placeholder.com/400x200?text=SpaceX+Launch",
        "category": "Technology",
        "ai_summary": "SpaceX successfully launched additional Starlink satellites, expanding the constellation and advancing global internet connectivity goals.",
        "key_points": [
            "SpaceX launches Starlink satellites",
            "Expands global internet coverage",
            "Successful mission completion"
        ],
        "reading_time": 3
    },
    {
        "title": "Climate Summit Reaches Historic Agreement",
        "description": "World leaders at the international climate summit have reached a groundbreaking agreement on carbon reduction targets and renewable energy investment.",
        "source": {"name": "Global News"},
        "publishedAt": "2024-01-15T06:20:00Z",
        "url": "https://example.com/climate-summit",
        "urlToImage": "https://via.placeholder.com/400x200?text=Climate+Summit",
        "category": "Politics",
        "ai_summary": "International climate summit resulted in a historic agreement with ambitious carbon reduction targets and significant renewable energy investment commitments.",
        "key_points": [
            "Historic climate agreement reached",
            "Ambitious carbon reduction targets",
            "Major renewable energy investments"
        ],
        "reading_time": 5
    }
]

def main():
    # Header
    st.markdown('<h1 class="main-header">📰 News Digest Demo</h1>', unsafe_allow_html=True)
    
    # Demo notice
    st.info("🎭 This is a demo version showing the application features with sample data. To use real news, set up API keys and run the full application.")
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="demo-card"><h3>🎯 Demo Features</h3></div>', unsafe_allow_html=True)
        
        st.subheader("📂 Sample Categories")
        categories = ["Technology", "Business", "Science", "Politics"]
        selected_categories = st.multiselect(
            "Choose categories:",
            categories,
            default=categories[:2]
        )
        
        st.subheader("📅 Update Frequency")
        frequency = st.selectbox(
            "Frequency:",
            ["daily", "weekly"],
            index=0
        )
        
        if st.button("🔄 Refresh Demo Data"):
            st.success("Demo data refreshed!")
        
        # Demo stats
        st.markdown('<div class="demo-card"><h3>📊 Demo Stats</h3></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Articles", len(SAMPLE_ARTICLES))
            st.metric("Categories", len(set(article['category'] for article in SAMPLE_ARTICLES)))
        with col2:
            st.metric("Avg Rating", "4.2")
            st.metric("Saved", "12")
    
    # Main content
    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Articles", len(SAMPLE_ARTICLES))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Categories", len(set(article['category'] for article in SAMPLE_ARTICLES)))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg Rating", "4.2/5")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Last Updated", datetime.now().strftime("%H:%M"))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # News feed
    st.header("📰 Sample News Feed")
    
    # Filter articles by selected categories
    filtered_articles = [article for article in SAMPLE_ARTICLES if article['category'] in selected_categories]
    
    # Group by category
    categorized_articles = {}
    for article in filtered_articles:
        category = article['category']
        if category not in categorized_articles:
            categorized_articles[category] = []
        categorized_articles[category].append(article)
    
    # Display articles
    for category, articles in categorized_articles.items():
        st.markdown(f'<div class="demo-card"><h3>📂 {category} ({len(articles)} articles)</h3></div>', unsafe_allow_html=True)
        
        for article in articles:
            display_demo_article(article)
    
    # Features showcase
    st.header("🚀 Application Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 AI-Powered Features")
        st.write("• **Smart Summarization**: AI-generated article summaries")
        st.write("• **Key Points Extraction**: Automatic identification of main points")
        st.write("• **Reading Time Estimation**: Time estimates for each article")
        st.write("• **Content Categorization**: Automatic article classification")
    
    with col2:
        st.subheader("📊 User Features")
        st.write("• **Personalized Feed**: Articles based on your interests")
        st.write("• **Save & Rate**: Save articles and rate them")
        st.write("• **Analytics Dashboard**: Track your reading patterns")
        st.write("• **Share Functionality**: Share articles with others")
    
    # Setup instructions
    st.header("🔧 Get Started")
    
    st.info("""
    **To use the full application with real news:**
    
    1. **Get API Keys**:
       - NewsAPI: https://newsapi.org/
       - Gemini API: https://makersuite.google.com/app/apikey
    
    2. **Set up the application**:
       ```bash
       python deploy.py setup
       # Edit .env file with your API keys
       python deploy.py test
       python deploy.py start
       ```
    
    3. **Deploy to production**:
       - Streamlit Cloud: share.streamlit.io
       - Netlify: netlify.com
       - Google Colab: Use the provided notebook
    """)

def display_demo_article(article):
    """Display a demo article card"""
    st.markdown('<div class="article-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(article['title'])
        
        # Article metadata
        published_date = article['publishedAt']
        source_name = article['source']['name']
        reading_time = article['reading_time']
        
        st.caption(f"📅 {published_date} | 📰 {source_name} | ⏱️ {reading_time} min read")
        
        # Article description
        st.write(article['description'])
        
        # AI Summary
        if article.get('ai_summary'):
            st.markdown(f'<div style="background-color: #e8f4fd; padding: 1rem; border-radius: 8px; border-left: 4px solid #1f77b4; margin: 1rem 0;"><strong>🤖 AI Summary:</strong><br>{article["ai_summary"]}</div>', unsafe_allow_html=True)
        
        # Key points
        if article.get('key_points'):
            st.subheader("🔑 Key Points:")
            for point in article['key_points']:
                st.write(f"• {point}")
        
        # Demo actions
        col_action1, col_action2, col_action3, col_action4 = st.columns(4)
        
        with col_action1:
            if st.button("💾 Save", key=f"save_{article['url']}"):
                st.success("Saved! (Demo)")
        
        with col_action2:
            rating = st.selectbox("⭐ Rate", [1, 2, 3, 4, 5], key=f"rate_{article['url']}")
            if st.button("Submit", key=f"submit_{article['url']}"):
                st.success(f"Rated {rating} stars! (Demo)")
        
        with col_action3:
            if st.button("📤 Share", key=f"share_{article['url']}"):
                st.write(f"Share: {article['url']} (Demo)")
        
        with col_action4:
            if st.button("🔗 Open", key=f"open_{article['url']}"):
                st.markdown(f"[Open Article]({article['url']}) (Demo)")
    
    with col2:
        # Article image
        st.image(article['urlToImage'], width=150)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
