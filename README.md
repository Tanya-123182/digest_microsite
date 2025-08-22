# Personalized News Digest Microsite

A modern dashboard-style news aggregation platform that provides personalized news summaries based on user interests and frequency preferences.

## Features

- **Personalized Dashboard**: User-friendly interface for selecting interests and frequency
- **Smart News Aggregation**: Scrapes news from multiple sources using NewsAPI
- **AI-Powered Summarization**: Uses Gemini API to generate concise summaries
- **Categorized Feed**: Organizes news by categories and user interests
- **Interactive Features**: Save, rate, and share digests
- **Responsive Design**: Works seamlessly across devices

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python (Streamlit)
- **APIs**: NewsAPI, Gemini API
- **Deployment**: Netlify
- **Development**: Google Colab integration

## Setup Instructions

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up API keys in `.env` file
4. Run the application: `streamlit run app.py`

## API Keys Required

- NewsAPI key (get from https://newsapi.org/)
- Gemini API key (get from https://makersuite.google.com/app/apikey)

## Project Structure

```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── static/               # Static assets
│   ├── css/
│   ├── js/
│   └── images/
├── components/           # Reusable components
├── utils/               # Utility functions
└── data/               # Data storage
```

## Usage

1. Select your news interests
2. Choose frequency (daily/weekly)
3. View personalized news digest
4. Save, rate, or share articles
5. Customize your preferences anytime

## License

MIT License
