import os
import tempfile
import json
import time
import requests
from datetime import datetime
from pathlib import Path

def create_temp_directory(prefix="news_analyzer_"):
    """
    Create a temporary directory for storing files
    
    Returns:
    str: Path to the temporary directory
    """
    temp_dir = os.path.join(tempfile.gettempdir(), f"{prefix}{int(time.time())}")
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

def save_json_data(data, filename, directory=None):
    """
    Save data as JSON file
    
    Parameters:
    data (dict): Data to save
    filename (str): Name of the file
    directory (str, optional): Directory to save the file, defaults to a temporary directory
    
    Returns:
    str: Path to the saved file
    """
    if directory is None:
        directory = tempfile.gettempdir()
    
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Create full file path
    file_path = os.path.join(directory, filename)
    
    # Save data to file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return file_path

def load_json_data(file_path):
    """
    Load data from JSON file
    
    Parameters:
    file_path (str): Path to the JSON file
    
    Returns:
    dict: Loaded data
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data

def get_audio_data_url(audio_path):
    """
    Convert audio file to base64 data URL for HTML audio element
    
    Parameters:
    audio_path (str): Path to the audio file
    
    Returns:
    str: Base64 data URL
    """
    import base64
    
    # Read the audio file
    with open(audio_path, 'rb') as audio_file:
        audio_data = audio_file.read()
    
    # Encode as base64
    encoded_audio = base64.b64encode(audio_data).decode('utf-8')
    
    # Create data URL
    data_url = f"data:audio/mp3;base64,{encoded_audio}"
    
    return data_url

def format_date(date_str):
    """
    Format date string to a readable format
    
    Parameters:
    date_str (str): Date string in ISO format
    
    Returns:
    str: Formatted date string
    """
    try:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str

def clean_text(text):
    """
    Clean text by removing extra whitespaces and newlines
    
    Parameters:
    text (str): Text to clean
    
    Returns:
    str: Cleaned text
    """
    import re
    
    # Replace multiple whitespaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespaces
    text = text.strip()
    
    return text

def truncate_text(text, max_length=100, add_ellipsis=True):
    """
    Truncate text to maximum length
    
    Parameters:
    text (str): Text to truncate
    max_length (int): Maximum length
    add_ellipsis (bool): Whether to add ellipsis
    
    Returns:
    str: Truncated text
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length].rsplit(' ', 1)[0]
    
    if add_ellipsis:
        truncated += "..."
    
    return truncated