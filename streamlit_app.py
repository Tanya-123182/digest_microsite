import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Import our utility modules
from utils import NewsAPIClient, GeminiAPIClient, DataManager

# Load environment variables
load_dotenv()

# Initialize clients
@st.cache_resource
def init_clients():
    """Initialize API clients with caching"""
    try:
        news_client = NewsAPIClient()
        gemini_client = GeminiAPIClient()
        data_manager = DataManager()
        return news_client, gemini_client, data_manager
    except Exception as e:
        st.error(f"Error initializing clients: {str(e)}")
        return None, None, None

# Page configuration
st.set_page_config(
    page_title="News Digest Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Global text color fix */
    .stApp {
        color: #2c3e50;
    }
    
    /* Main header with better contrast */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Category cards with dark text on light background */
    .category-card {
        background: linear-gradient(135deg, #ecf0f1 0%, #bdc3c7 100%);
        color: #2c3e50;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #bdc3c7;
    }
    
    /* Article cards with proper contrast */
    .article-card {
        background: #ffffff;
        color: #2c3e50;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        transition: transform 0.2s;
    }
    .article-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    /* Summary box with dark text */
    .summary-box {
        background: linear-gradient(135deg, #e8f4f8 0%, #f0f8ff 100%);
        color: #2c3e50;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #3498db;
    }
    
    /* Metric cards with white text on dark background */
    .metric-card {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Buttons with better styling */
    .stButton > button {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s;
        font-weight: 600;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        background: linear-gradient(135deg, #2980b9 0%, #1f5f8b 100%);
    }
    
    /* Sidebar headers */
    .sidebar-header {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    /* Stats container with better contrast */
    .stats-container {
        background: rgba(52, 73, 94, 0.1);
        color: #2c3e50;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #bdc3c7;
    }
    
    /* Fix for Streamlit text elements */
    .stMarkdown, .stText {
        color: #2c3e50 !important;
    }
    
    /* Fix for sidebar text */
    .css-1d391kg {
        color: #2c3e50 !important;
    }
    
    /* Better contrast for selectboxes and inputs */
    .stSelectbox > div > div {
        color: #2c3e50 !important;
    }
    
    /* Fix for multiselect */
    .stMultiSelect > div > div {
        color: #2c3e50 !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize clients
    news_client, gemini_client, data_manager = init_clients()
    
    if not all([news_client, gemini_client, data_manager]):
        st.error("Failed to initialize application. Please check your API keys.")
        return
    
    # Header
    st.markdown('<h1 class="main-header">📰 Personalized News Digest</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'Dashboard'
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-header"><h3>🎯 Navigation</h3></div>', unsafe_allow_html=True)
        
        # Navigation menu
        view = st.selectbox(
            "Choose View:",
            ['Dashboard', 'Saved Articles', 'Analytics', 'Settings'],
            index=['Dashboard', 'Saved Articles', 'Analytics', 'Settings'].index(st.session_state.current_view)
        )
        
        if view == 'Dashboard':
            st.session_state.current_view = 'Dashboard'
            show_dashboard_sidebar(news_client, gemini_client, data_manager)
        elif view == 'Saved Articles':
            st.session_state.current_view = 'Saved Articles'
            show_saved_sidebar(data_manager)
        elif view == 'Analytics':
            st.session_state.current_view = 'Analytics'
            show_analytics_sidebar(data_manager)
        elif view == 'Settings':
            st.session_state.current_view = 'Settings'
            show_settings_sidebar(data_manager)
    
    # Main content area
    if st.session_state.current_view == 'Dashboard':
        show_dashboard(news_client, gemini_client, data_manager)
    elif st.session_state.current_view == 'Saved Articles':
        show_saved_articles(data_manager)
    elif st.session_state.current_view == 'Analytics':
        show_analytics(data_manager)
    elif st.session_state.current_view == 'Settings':
        show_settings(data_manager)

def show_dashboard_sidebar(news_client, gemini_client, data_manager):
    """Show dashboard sidebar with preferences"""
    st.markdown('<div class="sidebar-header"><h3>⚙️ Preferences</h3></div>', unsafe_allow_html=True)
    
    # Load current preferences
    preferences = data_manager.load_user_preferences()
    
    # Interest selection
    st.subheader("📂 Select Interests")
    available_categories = ['Technology', 'Business', 'Science', 'Politics', 'Sports', 'Entertainment']
    selected_interests = st.multiselect(
        "Choose news categories:",
        available_categories,
        default=preferences.get('interests', [])
    )
    
    # Frequency selection
    st.subheader("📅 Update Frequency")
    frequency = st.selectbox(
        "How often would you like updates?",
        ['daily', 'weekly'],
        index=0 if preferences.get('frequency') == 'daily' else 1
    )
    
    # Update preferences
    if st.button("🔄 Update & Fetch News"):
        with st.spinner("Updating preferences and fetching news..."):
            # Save preferences
            preferences['interests'] = selected_interests
            preferences['frequency'] = frequency
            data_manager.save_user_preferences(preferences)
            
            # Fetch news
            if selected_interests:
                articles = news_client.fetch_articles_by_interests(selected_interests, frequency)
                
                # Enhance articles with AI summaries
                if articles:
                    articles = gemini_client.batch_summarize(articles, delay=0.5)
                
                st.session_state.news_data = articles
                st.success(f"✅ Fetched {len(articles)} articles!")
            else:
                st.warning("Please select at least one interest category.")
    
    # Quick stats
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    st.subheader("📊 Quick Stats")
    
    user_stats = data_manager.get_user_stats()
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Saved Articles", user_stats.get('total_saved_articles', 0))
        st.metric("Avg Rating", f"{user_stats.get('average_rating', 0):.1f}")
    
    with col2:
        st.metric("Total Ratings", user_stats.get('total_ratings', 0))
        st.metric("Top Category", user_stats.get('favorite_category', 'None'))
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard(news_client, gemini_client, data_manager):
    """Show main dashboard"""
    
    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Articles", len(st.session_state.get('news_data', [])))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        categories_count = len(set(article.get('category', 'Unknown') for article in st.session_state.get('news_data', [])))
        st.metric("Categories", categories_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        user_stats = data_manager.get_user_stats()
        st.metric("Avg Rating", f"{user_stats.get('average_rating', 0):.1f}/5")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Last Updated", datetime.now().strftime("%H:%M"))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # News feed
    if st.session_state.get('news_data'):
        st.header("📰 Your Personalized News Feed")
        
        # Categorize articles
        categorized_articles = {}
        for article in st.session_state.news_data:
            category = article.get('category', 'General')
            if category not in categorized_articles:
                categorized_articles[category] = []
            categorized_articles[category].append(article)
        
        # Display articles by category
        for category, articles in categorized_articles.items():
            st.markdown(f'<div class="category-card"><h3>📂 {category} ({len(articles)} articles)</h3></div>', unsafe_allow_html=True)
            
            for article in articles:
                display_enhanced_article_card(article, data_manager)
    else:
        st.info("👆 Select your interests and update preferences to see your personalized news feed!")

def display_enhanced_article_card(article, data_manager):
    """Display an enhanced article card with more features"""
    # Create unique key using article title, URL, and current timestamp
    import hashlib
    import time
    unique_string = f"{article.get('title', '')}{article.get('url', '')}{time.time()}"
    article_key = hashlib.md5(unique_string.encode()).hexdigest()[:8]
    
    st.markdown('<div class="article-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(article.get('title', 'No title'))
        
        # Article metadata
        published_date = article.get('publishedAt', 'Unknown date')
        source_name = article.get('source', {}).get('name', 'Unknown source')
        reading_time = article.get('reading_time', 2)
        
        st.caption(f"📅 {published_date} | 📰 {source_name} | ⏱️ {reading_time} min read")
        
        # Article description
        description = article.get('description', 'No description available.')
        st.write(description[:200] + "..." if len(description) > 200 else description)
        
        # AI Summary (if available)
        if article.get('ai_summary'):
            st.markdown(f'<div class="summary-box"><strong>🤖 AI Summary:</strong><br>{article.get("ai_summary")}</div>', unsafe_allow_html=True)
        
        # Key points (if available)
        if article.get('key_points'):
            st.subheader("🔑 Key Points:")
            for point in article.get('key_points', [])[:3]:
                st.write(f"• {point}")
        
        # Article actions
        col_action1, col_action2, col_action3, col_action4 = st.columns(4)
        
        with col_action1:
            if st.button("💾 Save", key=f"save_{article_key}"):
                if data_manager.save_article(article):
                    st.success("Saved!")
                else:
                    st.info("Already saved!")
        
        with col_action2:
            rating = st.selectbox("⭐ Rate", [1, 2, 3, 4, 5], key=f"rate_{article_key}")
            if st.button("Submit", key=f"submit_rate_{article_key}"):
                data_manager.save_rating(article.get('url', ''), rating)
                st.success(f"Rated {rating} stars!")
        
        with col_action3:
            if st.button("📤 Share", key=f"share_{article_key}"):
                st.write(f"Share this article: {article.get('url', '')}")
        
        with col_action4:
            if st.button("🔗 Open", key=f"open_{article_key}"):
                st.markdown(f"[Open Article]({article.get('url', '')})")
    
    with col2:
        # Article image
        if article.get('urlToImage'):
            st.image(article.get('urlToImage'), width=150)
        else:
            st.image("https://via.placeholder.com/150x100?text=No+Image", width=150)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_saved_sidebar(data_manager):
    """Show saved articles sidebar"""
    st.markdown('<div class="sidebar-header"><h3>📚 Saved Articles</h3></div>', unsafe_allow_html=True)
    
    saved_articles = data_manager.load_saved_articles()
    st.metric("Total Saved", len(saved_articles))
    
    if st.button("🗑️ Clear All Saved"):
        if st.button("Confirm Clear"):
            data_manager.clear_all_data()
            st.success("All saved articles cleared!")

def show_saved_articles(data_manager):
    """Show saved articles view"""
    st.header("📚 Your Saved Articles")
    
    saved_articles = data_manager.load_saved_articles()
    
    if not saved_articles:
        st.info("No saved articles yet. Start reading and save interesting articles!")
        return
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        categories = list(set(article.get('category', 'Unknown') for article in saved_articles))
        selected_category = st.selectbox("Filter by Category", ['All'] + categories)
    
    with col2:
        sort_by = st.selectbox("Sort by", ['Date Saved', 'Title', 'Category'])
    
    # Filter and sort articles
    filtered_articles = saved_articles
    if selected_category != 'All':
        filtered_articles = [a for a in saved_articles if a.get('category') == selected_category]
    
    # Sort articles
    if sort_by == 'Date Saved':
        filtered_articles.sort(key=lambda x: x.get('saved_at', ''), reverse=True)
    elif sort_by == 'Title':
        filtered_articles.sort(key=lambda x: x.get('title', ''))
    elif sort_by == 'Category':
        filtered_articles.sort(key=lambda x: x.get('category', ''))
    
    # Display articles
    for i, article in enumerate(filtered_articles):
        st.markdown('<div class="article-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.subheader(article.get('title', 'No title'))
            st.caption(f"📅 {article.get('publishedAt', 'Unknown date')} | 📰 {article.get('source', {}).get('name', 'Unknown source')}")
            st.write(article.get('description', 'No description available.'))
            
            if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                data_manager.remove_saved_article(article.get('url', ''))
                st.success("Article removed!")
                st.rerun()
        
        with col2:
            if article.get('urlToImage'):
                st.image(article.get('urlToImage'), width=100)
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_analytics_sidebar(data_manager):
    """Show analytics sidebar"""
    st.markdown('<div class="sidebar-header"><h3>📊 Analytics</h3></div>', unsafe_allow_html=True)
    
    user_stats = data_manager.get_user_stats()
    st.metric("Total Articles", user_stats.get('total_saved_articles', 0))
    st.metric("Average Rating", f"{user_stats.get('average_rating', 0):.1f}")

def show_analytics(data_manager):
    """Show analytics view"""
    st.header("📊 Your Reading Analytics")
    
    user_stats = data_manager.get_user_stats()
    saved_articles = data_manager.load_saved_articles()
    ratings = data_manager.load_ratings()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Saved", user_stats.get('total_saved_articles', 0))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Ratings", user_stats.get('total_ratings', 0))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg Rating", f"{user_stats.get('average_rating', 0):.1f}/5")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Top Category", user_stats.get('favorite_category', 'None'))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts
    if saved_articles:
        col1, col2 = st.columns(2)
        
        with col1:
            # Category distribution
            category_counts = {}
            for article in saved_articles:
                category = article.get('category', 'Unknown')
                category_counts[category] = category_counts.get(category, 0) + 1
            
            if category_counts:
                fig = px.pie(
                    values=list(category_counts.values()),
                    names=list(category_counts.keys()),
                    title="Articles by Category"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Rating distribution
            if ratings:
                rating_counts = {}
                for rating_data in ratings.values():
                    rating = rating_data.get('rating', 0)
                    rating_counts[rating] = rating_counts.get(rating, 0) + 1
                
                if rating_counts:
                    fig = px.bar(
                        x=list(rating_counts.keys()),
                        y=list(rating_counts.values()),
                        title="Rating Distribution",
                        labels={'x': 'Rating', 'y': 'Count'}
                    )
                    st.plotly_chart(fig, use_container_width=True)

def show_settings_sidebar(data_manager):
    """Show settings sidebar"""
    st.markdown('<div class="sidebar-header"><h3>⚙️ Settings</h3></div>', unsafe_allow_html=True)
    
    data_sizes = data_manager.get_data_size()
    total_size = sum(data_sizes.values())
    st.metric("Data Size", f"{total_size / 1024:.1f} KB")

def show_settings(data_manager):
    """Show settings view"""
    st.header("⚙️ Application Settings")
    
    # Data management
    st.subheader("📁 Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Export Data"):
            export_path = "user_data_export.json"
            if data_manager.export_data(export_path):
                st.success(f"Data exported to {export_path}")
            else:
                st.error("Export failed")
    
    with col2:
        if st.button("🗑️ Clear All Data"):
            if st.button("⚠️ Confirm Clear All"):
                if data_manager.clear_all_data():
                    st.success("All data cleared!")
                else:
                    st.error("Failed to clear data")
    
    # Data statistics
    st.subheader("📊 Data Statistics")
    data_sizes = data_manager.get_data_size()
    
    for name, size in data_sizes.items():
        st.metric(f"{name.title()} Size", f"{size / 1024:.1f} KB")
    
    # API status
    st.subheader("🔗 API Status")
    
    try:
        news_client, gemini_client, _ = init_clients()
        
        col1, col2 = st.columns(2)
        
        with col1:
            if news_client:
                st.success("✅ NewsAPI: Connected")
            else:
                st.error("❌ NewsAPI: Not connected")
        
        with col2:
            if gemini_client:
                model_info = gemini_client.get_model_info()
                if model_info.get('model_available'):
                    st.success("✅ Gemini API: Connected")
                else:
                    st.error("❌ Gemini API: Not available")
            else:
                st.error("❌ Gemini API: Not connected")
    
    except Exception as e:
        st.error(f"Error checking API status: {str(e)}")

if __name__ == "__main__":
    main()
