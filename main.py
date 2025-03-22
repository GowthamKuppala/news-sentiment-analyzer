import requests
from bs4 import BeautifulSoup
import nltk
import os
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import spacy
from collections import Counter
from gtts import gTTS
import tempfile
import os
from IPython.display import Audio, display
import threading

# Download NLTK resources (only needed once)
home_dir = os.getenv("USERPROFILE")  # On Windows, use USERPROFILE instead of HOME
nltk.data.path.append(os.path.join(home_dir, "nltk_data"))

# Load SpaCy model (run once)
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

LANGUAGE_CODES = {
    "1": {"name": "Telugu", "code": "te"},
    "2": {"name": "Hindi", "code": "hi"},
    "3": {"name": "English", "code": "en"},
    "4": {"name": "Malayalam", "code": "ml"},
    "5": {"name": "Tamil", "code": "ta"},
    "6": {"name": "Kannada", "code": "kn"}
}

def text_to_speech(text, language_code, output_file=None):
    """
    Convert text to speech using gTTS in the specified language
    
    Parameters:
    text (str): Text to convert to speech
    language_code (str): Language code for gTTS
    output_file (str, optional): Path to save the audio file. If None, a temporary file will be created.
    
    Returns:
    str: Path to the generated audio file
    """
    # If no output file is specified, create a temporary file
    if output_file is None:
        temp_dir = tempfile.gettempdir()
        output_file = os.path.join(temp_dir, f"speech_{language_code}.mp3")
    
    # Create gTTS object with specified language
    tts = gTTS(text=text, lang=language_code, slow=False)
    
    # Save the audio file
    tts.save(output_file)
    
    return output_file

def translate_sentiment_analysis(final_sentiment, language_code):
    """
    Translate the final sentiment analysis to the specified language
    
    Parameters:
    final_sentiment (str): The final sentiment analysis in English
    language_code (str): Language code
    
    Returns:
    str: Translated sentiment analysis
    """
    # Check for common patterns in sentiment analysis and translate them
    translated_sentiment = final_sentiment
    
    # For Telugu
    if language_code == "te":
        if "predominantly positive" in final_sentiment:
            return "వార్తలు ప్రధానంగా సానుకూలంగా ఉన్నాయి. " + \
                   final_sentiment.replace("Positive news about ", "").replace(" is particularly noteworthy.", " గురించి సానుకూల వార్తలు ప్రత్యేకంగా గమనార్హమైనవి.")
        elif "significant concerns" in final_sentiment:
            return "వార్తలు గణనీయమైన ఆందోళనలను చూపిస్తున్నాయి, ముఖ్యంగా " + \
                   final_sentiment.replace("Coverage shows significant concerns, particularly regarding ", "") + " విషయంలో."
        elif "cautiously positive" in final_sentiment:
            return "వార్తలు జాగ్రత్తగా సానుకూలంగా ఉన్నాయి, కొన్ని ఆందోళనలు " + \
                   final_sentiment.replace("Coverage is cautiously positive, with some concerns noted about ", "") + " గురించి గమనించబడ్డాయి."
        elif "leans negative" in final_sentiment:
            return "వార్తలు ప్రతికూలంగా మొగ్గు చూపుతున్నాయి, అయినప్పటికీ " + \
                   final_sentiment.replace("Coverage leans negative, though there are some positive developments in ", "") + " లో కొన్ని సానుకూల పరిణామాలు ఉన్నాయి."
        elif "mixed or neutral" in final_sentiment:
            return "వార్తలు మిశ్రమంగా లేదా తటస్థంగా ఉన్నాయి, " + \
                   final_sentiment.replace("Coverage is mixed or neutral, with balanced perspectives on ", "") + " పై సంతులిత దృక్కోణాలతో."
    
    # For Hindi
    elif language_code == "hi":
        if "predominantly positive" in final_sentiment:
            return "कवरेज मुख्य रूप से सकारात्मक है। " + \
                  final_sentiment.replace("Positive news about ", "").replace(" is particularly noteworthy.", " के बारे में सकारात्मक खबरें विशेष रूप से उल्लेखनीय हैं।")
        elif "significant concerns" in final_sentiment:
            return "कवरेज महत्वपूर्ण चिंताओं को दर्शाता है, विशेष रूप से " + \
                  final_sentiment.replace("Coverage shows significant concerns, particularly regarding ", "") + " के संबंध में।"
        elif "cautiously positive" in final_sentiment:
            return "कवरेज सावधानीपूर्वक सकारात्मक है, कुछ चिंताएं " + \
                  final_sentiment.replace("Coverage is cautiously positive, with some concerns noted about ", "") + " के बारे में नोट की गई हैं।"
        elif "leans negative" in final_sentiment:
            return "कवरेज नकारात्मक झुकाव वाला है, हालांकि " + \
                  final_sentiment.replace("Coverage leans negative, though there are some positive developments in ", "") + " में कुछ सकारात्मक विकास हैं।"
        elif "mixed or neutral" in final_sentiment:
            return "कवरेज मिश्रित या तटस्थ है, " + \
                  final_sentiment.replace("Coverage is mixed or neutral, with balanced perspectives on ", "") + " पर संतुलित दृष्टिकोण के साथ।"
    
    # For Malayalam
    elif language_code == "ml":
        if "predominantly positive" in final_sentiment:
            return "കവറേജ് പ്രധാനമായും പോസിറ്റീവാണ്. " + \
                  final_sentiment.replace("Positive news about ", "").replace(" is particularly noteworthy.", " എന്നതിനെക്കുറിച്ചുള്ള പോസിറ്റീവ് വാർത്തകൾ പ്രത്യേകിച്ച് ശ്രദ്ധേയമാണ്.")
        # Add other Malayalam translations as needed
    
    # For Tamil
    elif language_code == "ta":
        if "predominantly positive" in final_sentiment:
            return "உள்ளடக்கம் பெரும்பாலும் நேர்மறையானது. " + \
                  final_sentiment.replace("Positive news about ", "").replace(" is particularly noteworthy.", " பற்றிய நேர்மறை செய்திகள் குறிப்பிடத்தக்கவை.")
        # Add other Tamil translations as needed
    
    # For Kannada
    elif language_code == "kn":
        if "predominantly positive" in final_sentiment:
            return "ವರದಿಯು ಪ್ರಮುಖವಾಗಿ ಸಕಾರಾತ್ಮಕವಾಗಿದೆ. " + \
                  final_sentiment.replace("Positive news about ", "").replace(" is particularly noteworthy.", " ಬಗ್ಗೆ ಸಕಾರಾತ್ಮಕ ಸುದ್ದಿಗಳು ವಿಶೇಷವಾಗಿ ಗಮನಾರ್ಹವಾಗಿವೆ.")
        # Add other Kannada translations as needed
    
    # Return original for English or if no translation available
    return final_sentiment

def translate_summary(processed_data, language_code):
    """
    Generate a summary in the specified language
    
    Parameters:
    processed_data (dict): The processed news data with sentiment analysis
    language_code (str): Language code
    
    Returns:
    str: Translated summary text
    """
    company_name = processed_data["Company"]
    
    # Get sentiment distribution
    distribution = processed_data["Comparative Sentiment Score"]["Sentiment Distribution"]
    positive_count = distribution["Positive"]
    negative_count = distribution["Negative"]
    neutral_count = distribution["Neutral"]
    
    # Get final sentiment analysis and translate it
    final_sentiment = processed_data["Final Sentiment Analysis"]
    translated_sentiment = translate_sentiment_analysis(final_sentiment, language_code)
    
    # Get common topics
    common_topics = processed_data["Comparative Sentiment Score"]["Topic Overlap"]["Common Topics"]
    topics_text = ', '.join(common_topics[:3]) if common_topics else "No common topics found"
    
    # Basic translations based on language code
    if language_code == "hi":  # Hindi
        if "No common topics found" in topics_text:
            topics_text = "कोई सामान्य विषय नहीं मिला"
            
        summary = f"""
        {company_name} के बारे में समाचार विश्लेषण:
        
        हमने {len(processed_data["Articles"])} समाचार लेखों का विश्लेषण किया है।
        
        सकारात्मक लेख: {positive_count}
        नकारात्मक लेख: {negative_count}
        तटस्थ लेख: {neutral_count}
        
        समग्र विश्लेषण: {translated_sentiment}
        
        मुख्य विषय: {topics_text}
        """
    elif language_code == "te":  # Telugu
        if "No common topics found" in topics_text:
            topics_text = "సామాన్య అంశాలు కనుగొనబడలేదు"
            
        summary = f"""
        {company_name} గురించి వార్తా విశ్లేషణ:
        
        మేము {len(processed_data["Articles"])} వార్తా కథనాలను విశ్లేషించాము.
        
        సానుకూల వార్తలు: {positive_count}
        ప్రతికూల వార్తలు: {negative_count}
        తటస్థ వార్తలు: {neutral_count}
        
        మొత్తం విశ్లేషణ: {translated_sentiment}
        
        ప్రధాన అంశాలు: {topics_text}
        """
    elif language_code == "ml":  # Malayalam
        if "No common topics found" in topics_text:
            topics_text = "പൊതുവായ വിഷയങ്ങളൊന്നും കണ്ടെത്തിയില്ല"
            
        summary = f"""
        {company_name} എന്നതിനെക്കുറിച്ചുള്ള വാർത്താ വിശകലനം:
        
        ഞങ്ങൾ {len(processed_data["Articles"])} വാർത്താ ലേഖനങ്ങൾ വിശകലനം ചെയ്തു.
        
        പോസിറ്റീവ് ലേഖനങ്ങൾ: {positive_count}
        നെഗറ്റീവ് ലേഖനങ്ങൾ: {negative_count}
        നിഷ്പക്ഷ ലേഖനങ്ങൾ: {neutral_count}
        
        സമഗ്ര വിശകലനം: {translated_sentiment}
        
        പ്രധാന വിഷയങ്ങൾ: {topics_text}
        """
    elif language_code == "ta":  # Tamil
        if "No common topics found" in topics_text:
            topics_text = "பொதுவான தலைப்புகள் எதுவும் கண்டுபிடிக்கப்படவில்லை"
            
        summary = f"""
        {company_name} பற்றிய செய்தி பகுப்பாய்வு:
        
        நாங்கள் {len(processed_data["Articles"])} செய்தி கட்டுரைகளை ஆய்வு செய்துள்ளோம்.
        
        நேர்மறை கட்டுரைகள்: {positive_count}
        எதிர்மறை கட்டுரைகள்: {negative_count}
        நடுநிலை கட்டுரைகள்: {neutral_count}
        
        ஒட்டுமொத்த பகுப்பாய்வு: {translated_sentiment}
        
        முக்கிய தலைப்புகள்: {topics_text}
        """
    elif language_code == "kn":  # Kannada
        if "No common topics found" in topics_text:
            topics_text = "ಯಾವುದೇ ಸಾಮಾನ್ಯ ವಿಷಯಗಳು ಕಂಡುಬಂದಿಲ್ಲ"
            
        summary = f"""
        {company_name} ಕುರಿತು ಸುದ್ದಿ ವಿಶ್ಲೇಷಣೆ:
        
        ನಾವು {len(processed_data["Articles"])} ಸುದ್ದಿ ಲೇಖನಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಿದ್ದೇವೆ.
        
        ಸಕಾರಾತ್ಮಕ ಲೇಖನಗಳು: {positive_count}
        ನಕಾರಾತ್ಮಕ ಲೇಖನಗಳು: {negative_count}
        ತಟಸ್ಥ ಲೇಖನಗಳು: {neutral_count}
        
        ಒಟ್ಟಾರೆ ವಿಶ್ಲೇಷಣೆ: {translated_sentiment}
        
        ಪ್ರಮುಖ ವಿಷಯಗಳು: {topics_text}
        """
    else:  # English (default)
        summary = f"""
        News analysis for {company_name}:
        
        We have analyzed {len(processed_data["Articles"])} news articles.
        
        Positive articles: {positive_count}
        Negative articles: {negative_count}
        Neutral articles: {neutral_count}
        
        Overall analysis: {final_sentiment}
        
        Main topics: {topics_text}
        """
    
    return summary

# Add this to your main function or create a new function to generate speech
def generate_speech_for_analysis(processed_data):
    """
    Generate speech for the analysis results in the user's chosen language
    
    Parameters:
    processed_data (dict): The processed news data with sentiment analysis
    
    Returns:
    str: Path to the generated audio file
    """
    # Display language options
    print("\nSelect language for audio output:")
    for key, lang in LANGUAGE_CODES.items():
        print(f"{key}. {lang['name']}")
    
    # Get user choice
    while True:
        language_choice = input("Enter your choice (1-6): ")
        if language_choice in LANGUAGE_CODES:
            break
        print("Invalid choice. Please try again.")
    
    selected_language = LANGUAGE_CODES[language_choice]
    language_name = selected_language["name"]
    language_code = selected_language["code"]
    
    print(f"\nGenerating {language_name} speech...")
    
    # Generate summary in selected language
    summary_text = translate_summary(processed_data, language_code)
    
    # Convert to speech
    audio_file = text_to_speech(summary_text, language_code)
    
    print(f"\n{language_name} summary text:")
    print(summary_text)
    
    return audio_file, summary_text, language_name


def get_news_articles(query, num_articles=10):
    search_url = f"https://www.bing.com/news/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to retrieve news articles")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    seen_titles_and_summaries = set()  # Track combinations of title and summary
    
    for item in soup.select(".news-card")[:num_articles]:
        # Extract the title text from the <a> tag with class="title"
        title_tag = item.select_one("a.title")
        if title_tag:
            title = title_tag.text.strip()
            link = title_tag["href"] if title_tag.has_attr("href") else None
        else:
            # Fallback for other potential title elements
            title_tag = item.select_one("a")
            title = title_tag.text.strip() if title_tag else "No title available"
            link = title_tag["href"] if title_tag and title_tag.has_attr("href") else None
        
        summary_tag = item.select_one(".snippet")
        
        if title and link:
            summary = summary_tag.text.strip() if summary_tag else "No summary available"
            
            # Create a combined unique key of title + summary
            unique_key = (title, summary)
            
            # Check if the combination has been seen before to avoid duplicates
            if unique_key not in seen_titles_and_summaries:
                seen_titles_and_summaries.add(unique_key)
                # Using capitalized keys for consistency
                articles.append({"Title": title, "Link": link, "Summary": summary})
    
    return articles


def analyze_sentiment(text):
    # Using TextBlob
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    # Using VADER
    sid = SentimentIntensityAnalyzer()
    vader_scores = sid.polarity_scores(text)
    
    # Combine both approaches for more robust analysis
    if polarity > 0.1 or vader_scores['compound'] > 0.05:
        return "Positive"
    elif polarity < -0.1 or vader_scores['compound'] < -0.05:
        return "Negative"
    else:
        return "Neutral"

def extract_topics(text, num_topics=3):
    # Process with SpaCy
    doc = nlp(text)
    
    # Extract named entities
    entities = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT", "EVENT", "GPE", "WORK_OF_ART"]]
    
    # Extract key noun phrases
    noun_phrases = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) > 1]
    
    # Extract keywords using frequency
    words = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop and len(token.text) > 3]
    word_freq = Counter(words)
    keywords = [word for word, count in word_freq.most_common(5)]
    
    # Combine and select unique topics
    all_potential_topics = entities + noun_phrases + keywords
    
    # Clean and deduplicate topics
    clean_topics = []
    seen = set()
    for topic in all_potential_topics:
        topic = topic.strip().title()
        
        # Skip short topics and common articles/determiners
        if not topic or len(topic) < 4 or topic.lower() in ['the', 'this', 'that', 'these', 'those', 'already', 'an']:
            continue
            
        # Remove articles from the beginning
        if topic.lower().startswith('a ') or topic.lower().startswith('an ') or topic.lower().startswith('the '):
            topic = topic[topic.find(' ')+1:]
        
        # Add to clean topics if not seen before
        if topic.lower() not in seen and len(topic) > 3:
            seen.add(topic.lower())
            clean_topics.append(topic)
    
    # If we don't have enough topics, try to get the main subject
    if not clean_topics and len(text) > 0:
        # Try to extract the company or main subject from the text
        for token in doc:
            if token.pos_ == "PROPN" and len(token.text) > 3 and token.text.lower() not in seen:
                seen.add(token.text.lower())
                clean_topics.append(token.text.title())
                if len(clean_topics) >= num_topics:
                    break
    
    return clean_topics[:num_topics]

def perform_comparative_analysis(articles):
    # Calculate sentiment distribution
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment_counts[article["Sentiment"]] += 1
    
    # Find all topics across articles
    all_topics = set()
    for article in articles:
        all_topics.update(article["Topics"])
    
    # Find topic overlap
    topic_frequency = {topic: 0 for topic in all_topics}
    for article in articles:
        for topic in article["Topics"]:
            topic_frequency[topic] += 1
    
    common_topics = [topic for topic, count in topic_frequency.items() if count > 1]
    
    # Generate comparisons between articles
    comparisons = []
    if len(articles) >= 2:
        for i in range(len(articles)-1):
            for j in range(i+1, min(i+3, len(articles))):
                article1 = articles[i]
                article2 = articles[j]
                
                # Skip if both articles have the same sentiment
                if article1["Sentiment"] == article2["Sentiment"]:
                    continue
                
                # Get short version of titles for comparison (first 40 chars)
                title1 = article1["Title"][:40] + "..." if len(article1["Title"]) > 40 else article1["Title"]
                title2 = article2["Title"][:40] + "..." if len(article2["Title"]) > 40 else article2["Title"]
                
                comparison = {
                    "Comparison": f"Article '{title1}' has {article1['Sentiment'].lower()} sentiment, while '{title2}' has {article2['Sentiment'].lower()} sentiment.",
                    "Impact": generate_impact_statement(article1, article2)
                }
                comparisons.append(comparison)
    
    # Limit to most significant comparisons
    comparisons = comparisons[:3]
    
    # Create topic overlap analysis
    topic_overlap = {
        "Common Topics": common_topics,
        "Unique Topics": {}
    }
    
    # Find unique topics for each article
    for i, article in enumerate(articles):
        unique_topics = [topic for topic in article["Topics"] if topic_frequency[topic] == 1]
        topic_overlap["Unique Topics"][f"Article {i+1}"] = unique_topics
    
    # Generate final sentiment analysis
    final_sentiment = determine_overall_sentiment(sentiment_counts, articles)
    
    return {
        "Sentiment Distribution": sentiment_counts,
        "Coverage Differences": comparisons,
        "Topic Overlap": topic_overlap,
        "Final Sentiment Analysis": final_sentiment
    }

def generate_impact_statement(article1, article2):
    # Generate an impact statement based on article sentiments and topics
    if article1["Sentiment"] == "Positive" and article2["Sentiment"] == "Negative":
        return f"The positive news about {', '.join(article1['Topics'][:2])} is offset by concerns regarding {', '.join(article2['Topics'][:2])}."
    elif article1["Sentiment"] == "Negative" and article2["Sentiment"] == "Positive":
        return f"While there are concerns about {', '.join(article1['Topics'][:2])}, positive developments in {', '.join(article2['Topics'][:2])} may balance the overall impact."
    else:
        return f"The articles present different perspectives on {', '.join(set(article1['Topics'][:1] + article2['Topics'][:1]))}."

def determine_overall_sentiment(sentiment_counts, articles):
    # Determine overall sentiment based on distribution and article importance
    total = sum(sentiment_counts.values())
    
    if sentiment_counts["Positive"] > sentiment_counts["Negative"] + sentiment_counts["Neutral"]:
        return f"Coverage is predominantly positive. Positive news about {articles[0]['Topics'][0] if articles and articles[0]['Topics'] else 'the company'} is particularly noteworthy."
    elif sentiment_counts["Negative"] > sentiment_counts["Positive"] + sentiment_counts["Neutral"]:
        return f"Coverage shows significant concerns, particularly regarding {articles[0]['Topics'][0] if articles and articles[0]['Topics'] else 'the company'}."
    elif sentiment_counts["Positive"] > sentiment_counts["Negative"]:
        return f"Coverage is cautiously positive, with some concerns noted about {articles[0]['Topics'][0] if articles and articles[0]['Topics'] else 'the company'}."
    elif sentiment_counts["Negative"] > sentiment_counts["Positive"]:
        return f"Coverage leans negative, though there are some positive developments in {articles[0]['Topics'][0] if articles and articles[0]['Topics'] else 'the company'}."
    else:
        return f"Coverage is mixed or neutral, with balanced perspectives on {articles[0]['Topics'][0] if articles and articles[0]['Topics'] else 'the company'}."

def process_news_articles(company_name, news_articles):
    processed_articles = []
    
    for article in news_articles:
        # Extract title - Now using the correct capitalized key 'Title'
        title = article.get("Title", "Untitled")
        
        # Extract summary
        summary = article.get("Summary", "No summary available")
        
        # Perform sentiment analysis
        sentiment = analyze_sentiment(summary)
        
        # Extract topics
        topics = extract_topics(summary)
        
        processed_article = {
            "Title": title,
            "Summary": summary,
            "Sentiment": sentiment,
            "Topics": topics
        }
        
        processed_articles.append(processed_article)
    
    # Perform comparative analysis
    comparative_analysis = perform_comparative_analysis(processed_articles)
    
    # Create final output
    output = {
        "Company": company_name,
        "Articles": processed_articles,
        "Comparative Sentiment Score": comparative_analysis,
        "Final Sentiment Analysis": comparative_analysis["Final Sentiment Analysis"]
    }
    
    return output

# Modify your main function to include the speech generation
if __name__ == "__main__":
    company_name = input("Enter the company you want to know: ")
    news_articles = get_news_articles(company_name)
    
    # Process articles with sentiment and topic analysis
    processed_data = process_news_articles(company_name, news_articles)
    
    # Display detailed results in English
    print(f"\nAnalysis Results for {company_name}:\n")
    
    print("News Articles:")
    for i, article in enumerate(processed_data["Articles"], 1):
        # Display full title
        print(f"{i}. {article['Title']}")
        print(f"   Summary: {article['Summary']}")
        print(f"   Sentiment: {article['Sentiment']}")
        print(f"   Topics: {', '.join(article['Topics'])}")
        print("---")
    
    print("\nSentiment Distribution:")
    distribution = processed_data["Comparative Sentiment Score"]["Sentiment Distribution"]
    print(f"   Positive: {distribution['Positive']}")
    print(f"   Negative: {distribution['Negative']}")
    print(f"   Neutral: {distribution['Neutral']}")
    
    print("\nCoverage Differences:")
    for comparison in processed_data["Comparative Sentiment Score"]["Coverage Differences"]:
        print(f"   - {comparison['Comparison']}")
        print(f"     Impact: {comparison['Impact']}")
    
    print("\nTopic Overlap:")
    topic_overlap = processed_data["Comparative Sentiment Score"]["Topic Overlap"]
    if topic_overlap["Common Topics"]:
        print(f"   Common Topics: {', '.join(topic_overlap['Common Topics'])}")
    else:
        print("   Common Topics: None")
    
    print("\nFinal Sentiment Analysis:")
    print(f"   {processed_data['Final Sentiment Analysis']}")
    
    # Generate speech in user's chosen language
    audio_file, summary_text, language_name = generate_speech_for_analysis(processed_data)
    
    print(f"\n{language_name} speech saved to: {audio_file}")
    print("You can play this file using any media player.")