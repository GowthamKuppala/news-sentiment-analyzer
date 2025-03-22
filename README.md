---
title: News Sentiment Analyzer
emoji: 📰
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: "1.26.0"
app_file: app.py
pinned: false
---

# News Sentiment Analyzer with Multilingual TTS

This application analyzes news articles for a given company, performs sentiment analysis, and provides a text-to-speech summary in multiple Indian languages.

## Features

- Extracts and analyzes news articles about a specified company
- Performs sentiment analysis (positive, negative, neutral)
- Conducts comparative analysis across articles
- Extracts key topics from articles
- Generates text-to-speech summaries in multiple languages:
  - Telugu
  - Hindi
  - English
  - Malayalam
  - Tamil
  - Kannada
- Clean, responsive web interface with Streamlit

## Live Demo

The application is deployed on Hugging Face Spaces. You can access it here:
[News Analyzer Demo](https://huggingface.co/spaces/GowthamGK/Analyze_News)

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip or conda for package management

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/GowthamKuppala/news-sentiment-analyzer.git
   cd news-analyzer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download required NLTK and SpaCy resources:
   ```bash
   python -m nltk.downloader vader_lexicon punkt
   python -m spacy download en_core_web_sm
   ```

### Running the Application

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to http://localhost:8501

3. Enter a company name, select a language for TTS, and click "Analyze News"

### API Usage

The application includes a Flask API that can be used independently:

1. Start the API server:
   ```bash
   python api.py
   ```

2. Use the following endpoints:
   - `/api/news` (POST) - Analyze news for a company
   - `/api/speech` (POST) - Generate speech from processed data

Example API call using cURL:

```bash
curl -X POST http://localhost:5000/api/news \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Tesla"}'
```

### API Documentation using Postman

1. Import the Postman collection from the `postman` directory
2. Use the pre-configured requests to test the API

## Implementation Details

### Architecture

The application follows a modular architecture:

- `main.py` - Core functionality for news extraction and analysis
- `app.py` - Streamlit web interface
- `api.py` - Flask API for communication between frontend and backend
- `utils.py` - Utility functions

### Models Used

1. **Sentiment Analysis:**
   - NLTK VADER for sentiment scoring
   - TextBlob for additional polarity analysis
   - Combination approach for more robust sentiment classification

2. **Topic Extraction:**
   - SpaCy for named entity recognition and part-of-speech tagging
   - Frequency-based keyword extraction
   - Named entity and noun phrase extraction

3. **Text-to-Speech:**
   - Google Text-to-Speech (gTTS) for multilingual audio generation

### Data Flow

1. User inputs a company name through the Streamlit interface
2. The application fetches relevant news articles using web scraping
3. Each article is analyzed for sentiment and key topics
4. A comparative analysis is performed across all articles
5. The summary is translated to the selected language
6. Text-to-speech conversion generates an audio file
7. Results are displayed on the web interface

## Limitations and Assumptions

- **News Sources:** The application fetches news from Bing search results, which may have limitations in coverage and depth.
- **Sentiment Analysis:** The sentiment analysis is based on lexical methods which may not capture complex nuances or context-specific sentiments.
- **Language Support:** While the application supports multiple languages for TTS, the translation quality varies by language.
- **Rate Limiting:** Excessive usage may trigger rate limiting from the news sources or TTS service.
- **Web Scraping:** The web scraping approach is dependent on the current structure of the news websites and may require updates if they change.

## Future Improvements

- Add more sophisticated NLP models for sentiment analysis
- Expand language support for translations
- Implement caching for frequently searched companies
- Add historical data tracking and trend analysis
- Improve topic clustering and extraction algorithms

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NLTK, SpaCy, and TextBlob for NLP capabilities
- Google Text-to-Speech for multilingual TTS
- Streamlit for the web interface
- BeautifulSoup for web scraping