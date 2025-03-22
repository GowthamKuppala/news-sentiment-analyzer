from flask import Flask, request, jsonify
import os
import sys
import tempfile
import threading
from main import get_news_articles, process_news_articles, generate_speech_for_analysis

# Create Flask app instance
app = Flask(__name__)

@app.route('/api/news', methods=['POST'])
def news_api():
    """API endpoint to fetch and analyze news articles for a given company"""
    try:
        # Get company name from request
        data = request.json
        company_name = data.get('company_name')
        
        if not company_name:
            return jsonify({'error': 'Company name is required'}), 400
        
        # Get news articles
        news_articles = get_news_articles(company_name)
        
        # Process news articles
        processed_data = process_news_articles(company_name, news_articles)
        
        return jsonify(processed_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/speech', methods=['POST'])
def speech_api():
    """API endpoint to generate speech from processed news data"""
    try:
        # Get processed data and language choice from request
        data = request.json
        processed_data = data.get('processed_data')
        language_choice = data.get('language_choice', '3')  # Default to English (3)
        
        if not processed_data:
            return jsonify({'error': 'Processed data is required'}), 400
        
        # Generate speech
        audio_file, summary_text, language_name = generate_speech_for_analysis_api(processed_data, language_choice)
        
        return jsonify({
            'audio_path': audio_file,
            'summary_text': summary_text,
            'language': language_name
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_speech_for_analysis_api(processed_data, language_choice):
    """Modified version of generate_speech_for_analysis that doesn't require user input"""
    from main import LANGUAGE_CODES, text_to_speech, translate_summary
    
    selected_language = LANGUAGE_CODES[language_choice]
    language_name = selected_language["name"]
    language_code = selected_language["code"]
    
    # Generate summary in selected language
    summary_text = translate_summary(processed_data, language_code)
    
    # Convert to speech
    audio_file = text_to_speech(summary_text, language_code)
    
    return audio_file, summary_text, language_name

# Functions for direct import into Streamlit app
def summarize_news(company_name):
    """Get and analyze news for a company"""
    try:
        # Get news articles
        news_articles = get_news_articles(company_name)
        
        if not news_articles:
            return None
        
        # Process news articles
        processed_data = process_news_articles(company_name, news_articles)
        
        return processed_data
    
    except Exception as e:
        print(f"Error in summarize_news: {str(e)}")
        return None

def generate_speech(processed_data, language_choice):
    """Generate speech from processed data"""
    try:
        from main import LANGUAGE_CODES, text_to_speech, translate_summary
        
        selected_language = LANGUAGE_CODES[language_choice]
        language_code = selected_language["code"]
        
        # Generate summary in selected language
        summary_text = translate_summary(processed_data, language_code)
        
        # Convert to speech
        audio_file = text_to_speech(summary_text, language_code)
        
        return audio_file, summary_text
    
    except Exception as e:
        print(f"Error in generate_speech: {str(e)}")
        raise e

# Only run the Flask app if this file is executed directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)