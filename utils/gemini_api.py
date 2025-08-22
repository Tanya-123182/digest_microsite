import google.generativeai as genai
import os
from typing import Dict, List, Optional
import time

class GeminiAPIClient:
    """Client for interacting with Gemini API for text summarization and analysis"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def summarize_article(self, title: str, content: str, max_length: int = 200) -> str:
        """Summarize an article with enhanced context"""
        try:
            # Clean and prepare content
            clean_content = self._clean_content(content)
            
            prompt = f"""
            Please provide a concise and engaging summary of this news article in {max_length} words or less:
            
            Title: {title}
            Content: {clean_content[:1500]}...
            
            Requirements:
            - Focus on the key facts and main story
            - Make it engaging and informative
            - Include the most important details
            - Use clear, concise language
            - Maintain journalistic tone
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return f"Summary unavailable: {str(e)}"
    
    def summarize_article_object(self, article: dict, max_length: int = 200) -> str:
        """Summarize an article object directly"""
        try:
            title = article.get('title', '')
            content = article.get('description', '') or article.get('content', '')
            return self.summarize_article(title, content, max_length)
        except Exception as e:
            return f"Summary unavailable: {str(e)}"
    
    def categorize_article(self, title: str, content: str) -> str:
        """Categorize an article based on its content"""
        try:
            clean_content = self._clean_content(content)
            
            prompt = f"""
            Based on the title and content, categorize this article into one of these categories:
            - Technology
            - Business
            - Science
            - Politics
            - Sports
            - Entertainment
            
            Title: {title}
            Content: {clean_content[:1000]}...
            
            Respond with only the category name.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return "General"
    
    def extract_key_points(self, title: str, content: str) -> List[str]:
        """Extract key points from an article"""
        try:
            clean_content = self._clean_content(content)
            
            prompt = f"""
            Extract 3-5 key points from this news article:
            
            Title: {title}
            Content: {clean_content[:1000]}...
            
            Format as a bulleted list with concise points.
            """
            
            response = self.model.generate_content(prompt)
            # Parse bullet points
            points = [point.strip().lstrip('- ').lstrip('• ') 
                     for point in response.text.split('\n') 
                     if point.strip().startswith(('-', '•'))]
            return points[:5]  # Limit to 5 points
            
        except Exception as e:
            return ["Key points unavailable"]
    
    def generate_digest_summary(self, articles: List[Dict]) -> str:
        """Generate a summary of multiple articles for a digest"""
        try:
            if not articles:
                return "No articles to summarize."
            
            # Prepare article summaries
            article_summaries = []
            for i, article in enumerate(articles[:10], 1):  # Limit to 10 articles
                title = article.get('title', 'Unknown title')
                category = article.get('category', 'General')
                article_summaries.append(f"{i}. {category}: {title}")
            
            prompt = f"""
            Create a brief digest summary of these news articles:
            
            {chr(10).join(article_summaries)}
            
            Provide a 2-3 sentence overview highlighting the main themes and most important stories.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return f"Digest summary unavailable: {str(e)}"
    
    def analyze_sentiment(self, title: str, content: str) -> Dict:
        """Analyze the sentiment of an article"""
        try:
            clean_content = self._clean_content(content)
            
            prompt = f"""
            Analyze the sentiment of this news article and provide:
            1. Overall sentiment (Positive, Negative, Neutral)
            2. Confidence level (High, Medium, Low)
            3. Brief explanation
            
            Title: {title}
            Content: {clean_content[:1000]}...
            
            Format your response as:
            Sentiment: [sentiment]
            Confidence: [confidence]
            Explanation: [brief explanation]
            """
            
            response = self.model.generate_content(prompt)
            
            # Parse the response
            lines = response.text.strip().split('\n')
            sentiment_data = {}
            
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    sentiment_data[key.strip()] = value.strip()
            
            return sentiment_data
            
        except Exception as e:
            return {
                'Sentiment': 'Unknown',
                'Confidence': 'Low',
                'Explanation': f'Analysis failed: {str(e)}'
            }
    
    def generate_reading_time(self, content: str) -> int:
        """Estimate reading time in minutes"""
        try:
            # Average reading speed: 200-250 words per minute
            word_count = len(content.split())
            reading_time = max(1, word_count // 225)  # Conservative estimate
            return reading_time
        except:
            return 2  # Default fallback
    
    def _clean_content(self, content: str) -> str:
        """Clean and prepare content for processing"""
        if not content:
            return ""
        
        # Remove extra whitespace and normalize
        cleaned = ' '.join(content.split())
        
        # Remove common HTML artifacts
        cleaned = cleaned.replace('&nbsp;', ' ')
        cleaned = cleaned.replace('&amp;', '&')
        cleaned = cleaned.replace('&lt;', '<')
        cleaned = cleaned.replace('&gt;', '>')
        
        return cleaned
    
    def batch_summarize(self, articles: List[Dict], delay: float = 1.0) -> List[Dict]:
        """Summarize multiple articles with rate limiting"""
        summarized_articles = []
        
        for article in articles:
            try:
                title = article.get('title', '')
                content = article.get('content', '')
                
                # Generate summary
                summary = self.summarize_article(title, content)
                article['ai_summary'] = summary
                
                # Extract key points
                key_points = self.extract_key_points(title, content)
                article['key_points'] = key_points
                
                # Estimate reading time
                reading_time = self.generate_reading_time(content)
                article['reading_time'] = reading_time
                
                summarized_articles.append(article)
                
                # Rate limiting
                time.sleep(delay)
                
            except Exception as e:
                print(f"Error summarizing article '{article.get('title', 'Unknown')}': {str(e)}")
                article['ai_summary'] = "Summary unavailable"
                article['key_points'] = ["Key points unavailable"]
                article['reading_time'] = 2
                summarized_articles.append(article)
        
        return summarized_articles
    
    def get_model_info(self) -> Dict:
        """Get information about the current model"""
        try:
            return {
                'model_name': 'gemini-pro',
                'api_key_configured': bool(self.api_key),
                'model_available': True
            }
        except Exception as e:
            return {
                'model_name': 'unknown',
                'api_key_configured': bool(self.api_key),
                'model_available': False,
                'error': str(e)
            }
