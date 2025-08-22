import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd

class DataManager:
    """Manages user data, preferences, and article storage"""
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        self.ensure_data_directory()
        
        # File paths
        self.preferences_file = os.path.join(data_dir, "user_preferences.json")
        self.saved_articles_file = os.path.join(data_dir, "saved_articles.json")
        self.ratings_file = os.path.join(data_dir, "ratings.json")
        self.analytics_file = os.path.join(data_dir, "analytics.json")
        
    def ensure_data_directory(self):
        """Ensure the data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_user_preferences(self, preferences: Dict) -> bool:
        """Save user preferences to file"""
        try:
            preferences['last_updated'] = datetime.now().isoformat()
            
            with open(self.preferences_file, 'w') as f:
                json.dump(preferences, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving preferences: {str(e)}")
            return False
    
    def load_user_preferences(self) -> Dict:
        """Load user preferences from file"""
        default_preferences = {
            'interests': [],
            'frequency': 'daily',
            'notifications': True,
            'theme': 'light',
            'last_updated': None
        }
        
        try:
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r') as f:
                    preferences = json.load(f)
                return preferences
            else:
                return default_preferences
        except Exception as e:
            print(f"Error loading preferences: {str(e)}")
            return default_preferences
    
    def save_article(self, article: Dict) -> bool:
        """Save an article to the user's saved list"""
        try:
            saved_articles = self.load_saved_articles()
            
            # Check if article already exists
            article_id = article.get('url', '')
            if not any(a.get('url') == article_id for a in saved_articles):
                article['saved_at'] = datetime.now().isoformat()
                saved_articles.append(article)
                
                with open(self.saved_articles_file, 'w') as f:
                    json.dump(saved_articles, f, indent=2)
                return True
            return False
        except Exception as e:
            print(f"Error saving article: {str(e)}")
            return False
    
    def load_saved_articles(self) -> List[Dict]:
        """Load saved articles from file"""
        try:
            if os.path.exists(self.saved_articles_file):
                with open(self.saved_articles_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading saved articles: {str(e)}")
            return []
    
    def remove_saved_article(self, article_url: str) -> bool:
        """Remove an article from saved list"""
        try:
            saved_articles = self.load_saved_articles()
            saved_articles = [a for a in saved_articles if a.get('url') != article_url]
            
            with open(self.saved_articles_file, 'w') as f:
                json.dump(saved_articles, f, indent=2)
            return True
        except Exception as e:
            print(f"Error removing article: {str(e)}")
            return False
    
    def save_rating(self, article_url: str, rating: int, user_comment: str = "") -> bool:
        """Save a user rating for an article"""
        try:
            ratings = self.load_ratings()
            
            ratings[article_url] = {
                'rating': rating,
                'comment': user_comment,
                'rated_at': datetime.now().isoformat()
            }
            
            with open(self.ratings_file, 'w') as f:
                json.dump(ratings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving rating: {str(e)}")
            return False
    
    def load_ratings(self) -> Dict:
        """Load user ratings from file"""
        try:
            if os.path.exists(self.ratings_file):
                with open(self.ratings_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading ratings: {str(e)}")
            return {}
    
    def get_article_rating(self, article_url: str) -> Optional[Dict]:
        """Get rating for a specific article"""
        ratings = self.load_ratings()
        return ratings.get(article_url)
    
    def save_analytics(self, analytics_data: Dict) -> bool:
        """Save analytics data"""
        try:
            analytics_data['timestamp'] = datetime.now().isoformat()
            
            # Load existing analytics
            existing_analytics = self.load_analytics()
            existing_analytics.append(analytics_data)
            
            # Keep only last 100 entries
            if len(existing_analytics) > 100:
                existing_analytics = existing_analytics[-100:]
            
            with open(self.analytics_file, 'w') as f:
                json.dump(existing_analytics, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving analytics: {str(e)}")
            return False
    
    def load_analytics(self) -> List[Dict]:
        """Load analytics data"""
        try:
            if os.path.exists(self.analytics_file):
                with open(self.analytics_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading analytics: {str(e)}")
            return []
    
    def get_user_stats(self) -> Dict:
        """Get user statistics"""
        try:
            saved_articles = self.load_saved_articles()
            ratings = self.load_ratings()
            preferences = self.load_user_preferences()
            
            # Calculate average rating
            avg_rating = 0
            if ratings:
                total_rating = sum(r['rating'] for r in ratings.values())
                avg_rating = total_rating / len(ratings)
            
            # Get category preferences
            category_counts = {}
            for article in saved_articles:
                category = article.get('category', 'Unknown')
                category_counts[category] = category_counts.get(category, 0) + 1
            
            return {
                'total_saved_articles': len(saved_articles),
                'total_ratings': len(ratings),
                'average_rating': round(avg_rating, 1),
                'favorite_category': max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else 'None',
                'interests': preferences.get('interests', []),
                'frequency': preferences.get('frequency', 'daily'),
                'last_activity': preferences.get('last_updated')
            }
        except Exception as e:
            print(f"Error getting user stats: {str(e)}")
            return {}
    
    def export_data(self, export_path: str) -> bool:
        """Export all user data to a JSON file"""
        try:
            export_data = {
                'preferences': self.load_user_preferences(),
                'saved_articles': self.load_saved_articles(),
                'ratings': self.load_ratings(),
                'analytics': self.load_analytics(),
                'exported_at': datetime.now().isoformat()
            }
            
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting data: {str(e)}")
            return False
    
    def import_data(self, import_path: str) -> bool:
        """Import user data from a JSON file"""
        try:
            with open(import_path, 'r') as f:
                import_data = json.load(f)
            
            # Validate import data
            required_keys = ['preferences', 'saved_articles', 'ratings']
            if not all(key in import_data for key in required_keys):
                raise ValueError("Invalid import file format")
            
            # Save imported data
            self.save_user_preferences(import_data['preferences'])
            
            with open(self.saved_articles_file, 'w') as f:
                json.dump(import_data['saved_articles'], f, indent=2)
            
            with open(self.ratings_file, 'w') as f:
                json.dump(import_data['ratings'], f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error importing data: {str(e)}")
            return False
    
    def clear_all_data(self) -> bool:
        """Clear all user data"""
        try:
            files_to_remove = [
                self.preferences_file,
                self.saved_articles_file,
                self.ratings_file,
                self.analytics_file
            ]
            
            for file_path in files_to_remove:
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            return True
        except Exception as e:
            print(f"Error clearing data: {str(e)}")
            return False
    
    def get_data_size(self) -> Dict:
        """Get size information for all data files"""
        try:
            sizes = {}
            files = {
                'preferences': self.preferences_file,
                'saved_articles': self.saved_articles_file,
                'ratings': self.ratings_file,
                'analytics': self.analytics_file
            }
            
            for name, file_path in files.items():
                if os.path.exists(file_path):
                    size = os.path.getsize(file_path)
                    sizes[name] = size
                else:
                    sizes[name] = 0
            
            return sizes
        except Exception as e:
            print(f"Error getting data size: {str(e)}")
            return {}
