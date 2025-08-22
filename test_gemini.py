#!/usr/bin/env python3
"""
Test script to troubleshoot Gemini API issues
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_gemini_api():
    """Test Gemini API connection and functionality"""
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    
    print("🔍 Testing Gemini API...")
    print(f"API Key found: {'✅ Yes' if api_key else '❌ No'}")
    
    if not api_key:
        print("\n❌ No Gemini API key found!")
        print("Please set GEMINI_API_KEY in your .env file")
        return False
    
    if api_key == "YOUR_NEW_GEMINI_API_KEY_HERE":
        print("\n❌ API key is still the placeholder!")
        print("Please replace with your actual Gemini API key")
        return False
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Test model availability
        print("\n📡 Testing model availability...")
        model = genai.GenerativeModel('gemini-pro')
        
        # Test simple generation
        print("🤖 Testing text generation...")
        response = model.generate_content("Say 'Hello, Gemini API is working!'")
        
        if response.text:
            print(f"✅ Success! Response: {response.text}")
            return True
        else:
            print("❌ No response received")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        
        # Common error messages and solutions
        if "404" in str(e):
            print("\n💡 Solution: Your API key might be invalid or expired")
            print("   Get a new key from: https://makersuite.google.com/app/apikey")
        elif "quota" in str(e).lower():
            print("\n💡 Solution: You've exceeded your API quota")
            print("   Check your usage at: https://makersuite.google.com/app/apikey")
        elif "permission" in str(e).lower():
            print("\n💡 Solution: API key doesn't have proper permissions")
            print("   Make sure you have access to gemini-pro model")
        
        return False

def get_new_api_key_instructions():
    """Print instructions for getting a new API key"""
    print("\n" + "="*50)
    print("🔑 How to Get a New Gemini API Key:")
    print("="*50)
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the new API key")
    print("5. Update your .env file:")
    print("   GEMINI_API_KEY=your_new_key_here")
    print("6. Restart your app")
    print("="*50)

if __name__ == "__main__":
    print("🚀 Gemini API Troubleshooter")
    print("="*30)
    
    success = test_gemini_api()
    
    if not success:
        get_new_api_key_instructions()
    else:
        print("\n🎉 Gemini API is working correctly!")
        print("Your app should now have AI features enabled.")
