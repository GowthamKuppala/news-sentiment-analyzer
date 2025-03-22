import streamlit as st
import requests
from api import summarize_news, generate_speech
import base64
import os
import tempfile

st.set_page_config(
    page_title="News Analyzer with TTS",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
    .sentiment-positive {
        color: #10B981;
        font-weight: bold;
    }
    .sentiment-negative {
        color: #EF4444;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: #6B7280;
        font-weight: bold;
    }
    .company-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #F3F4F6;
        margin-bottom: 1rem;
    }
    .article-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("📰 News Sentiment Analyzer with Multilingual TTS")
st.markdown("Get sentiment analysis of news articles for any company with text-to-speech output in multiple languages.")

# Input section
st.header("Enter Company Details")
company_name = st.text_input("Company Name", placeholder="e.g., Tesla, Apple, Google")

# Language selection for TTS
st.subheader("Select Language for Text-to-Speech")
language_options = {
    "1": "Telugu",
    "2": "Hindi",
    "3": "English",
    "4": "Malayalam",
    "5": "Tamil",
    "6": "Kannada"
}
language_choice = st.selectbox("Language", options=list(language_options.values()), index=2)
# Map back to the key
language_key = [k for k, v in language_options.items() if v == language_choice][0]

# Search button
if st.button("Analyze News", type="primary"):
    if company_name:
        with st.spinner(f"Fetching and analyzing news for {company_name}..."):
            try:
                # Call the API to get news analysis
                news_data = summarize_news(company_name)
                
                if news_data and "Articles" in news_data and len(news_data["Articles"]) > 0:
                    st.success(f"Successfully analyzed {len(news_data['Articles'])} news articles for {company_name}")
                    
                    # Display company overview
                    st.header(f"Analysis for {company_name}")
                    
                    # Create tabs for different sections
                    tab1, tab2, tab3 = st.tabs(["Summary", "Detailed Analysis", "Articles"])
                    
                    with tab1:
                        # Display sentiment distribution
                        st.subheader("Sentiment Distribution")
                        distribution = news_data["Comparative Sentiment Score"]["Sentiment Distribution"]
                        
                        # Calculate percentages
                        total = sum(distribution.values())
                        if total > 0:
                            positive_pct = round(distribution["Positive"] / total * 100)
                            negative_pct = round(distribution["Negative"] / total * 100)
                            neutral_pct = round(distribution["Neutral"] / total * 100)
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Positive", f"{distribution['Positive']} ({positive_pct}%)")
                            with col2:
                                st.metric("Negative", f"{distribution['Negative']} ({negative_pct}%)")
                            with col3:
                                st.metric("Neutral", f"{distribution['Neutral']} ({neutral_pct}%)")
                        
                        # Display final sentiment analysis
                        st.subheader("Overall Sentiment")
                        st.markdown(f"**{news_data['Final Sentiment Analysis']}**")
                        
                        # Display common topics
                        st.subheader("Main Topics")
                        common_topics = news_data["Comparative Sentiment Score"]["Topic Overlap"]["Common Topics"]
                        if common_topics:
                            st.write(", ".join(common_topics[:5]))
                        else:
                            st.write("No common topics found across articles")
                            
                        # Generate audio for the selected language
                        st.subheader(f"Audio Summary in {language_choice}")
                        with st.spinner(f"Generating {language_choice} speech..."):
                            audio_path, summary_text = generate_speech(news_data, language_key)
                            
                            # Display the summary text
                            st.text_area("Summary Text", summary_text, height=200)
                            
                            # Display audio player
                            with open(audio_path, "rb") as audio_file:
                                audio_bytes = audio_file.read()
                                st.audio(audio_bytes, format="audio/mp3")
                                
                                # Add download button for the audio
                                st.download_button(
                                    label=f"Download {language_choice} Audio",
                                    data=audio_bytes,
                                    file_name=f"{company_name}_summary_{language_choice.lower()}.mp3",
                                    mime="audio/mp3"
                                )
                    
                    with tab2:
                        # Display comparative analysis
                        st.subheader("Coverage Differences")
                        for comparison in news_data["Comparative Sentiment Score"]["Coverage Differences"]:
                            st.markdown(f"**{comparison['Comparison']}**")
                            st.markdown(f"*Impact:* {comparison['Impact']}")
                            st.markdown("---")
                        
                        # Display topic overlap
                        st.subheader("Topic Analysis")
                        topic_overlap = news_data["Comparative Sentiment Score"]["Topic Overlap"]
                        
                        # Common topics
                        if topic_overlap["Common Topics"]:
                            st.markdown("**Common Topics Across Articles:**")
                            st.write(", ".join(topic_overlap["Common Topics"]))
                        
                        # Unique topics
                        if "Unique Topics" in topic_overlap and topic_overlap["Unique Topics"]:
                            st.markdown("**Unique Topics by Article:**")
                            for article_id, topics in topic_overlap["Unique Topics"].items():
                                if topics:
                                    st.markdown(f"*{article_id}:* {', '.join(topics)}")
                    
                    with tab3:
                        # Display individual articles
                        st.subheader("Individual Article Analysis")
                        
                        for i, article in enumerate(news_data["Articles"], 1):
                            with st.expander(f"Article {i}: {article['Title']}"):
                                # Determine sentiment color
                                sentiment_class = f"sentiment-{article['Sentiment'].lower()}"
                                
                                st.markdown(f"**Summary:** {article['Summary']}")
                                st.markdown(f"**Sentiment:** <span class='{sentiment_class}'>{article['Sentiment']}</span>", unsafe_allow_html=True)
                                st.markdown(f"**Topics:** {', '.join(article['Topics'])}")
                else:
                    st.error(f"No news articles found for {company_name} or analysis failed.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a company name to analyze.")

# Add information about the app
with st.sidebar:
    st.header("About this App")
    st.markdown("""
    This application analyzes recent news articles about a company and provides:
    
    - Sentiment analysis (positive, negative, neutral)
    - Topic extraction
    - Comparative analysis across articles
    - Text-to-speech summary in multiple languages
    
    ### How to Use
    1. Enter a company name
    2. Select your preferred language for the audio summary
    3. Click "Analyze News"
    4. Explore the analysis in the tabs
    5. Listen to or download the audio summary
    
    ### Supported Languages
    - Telugu
    - Hindi
    - English
    - Malayalam
    - Tamil
    - Kannada
    """)
    
    st.markdown("---")
    st.markdown("© 2025 News Analyzer - Akaike Internship Project")