# Hugging Face Spaces Deployment

This document provides step-by-step instructions for deploying the News Analyzer application on Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account
2. Git installed on your computer
3. Complete, working code for the application

## Deployment Steps

### 1. Prepare Your Repository

Ensure your repository has the following structure:
```
news-analyzer/
├── app.py              # Streamlit application
├── api.py              # API implementation
├── main.py             # Core functionality
├── utils.py            # Utility functions
├── requirements.txt    # Dependencies
├── README.md           # Documentation
└── .gitignore          # Git ignore file
```

### 2. Create a Hugging Face Space

1. Go to [Hugging Face](https://huggingface.co/) and sign in
2. Click on your profile picture and select "New Space"
3. Fill in the details:
   - **Owner**: Your username or organization
   - **Space name**: "news-analyzer" (or your preferred name)
   - **License**: Choose an appropriate license (e.g., MIT)
   - **SDK**: Select "Streamlit"
   - **Space hardware**: Choose hardware based on your needs (CPU is sufficient)
   - **Privacy**: Public or Private as needed

4. Click "Create Space"

### 3. Clone Your Space Repository

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/news-analyzer
cd news-analyzer
```

### 4. Configure the Space for Streamlit

Create a file named `app.py` in the root with your Streamlit code.

### 5. Add Dependencies to requirements.txt

```
streamlit==1.30.0
beautifulsoup4==4.12.2
nltk==3.8.1
textblob==0.17.1
spacy==3.7.2
gtts==2.4.0
requests==2.31.0
pandas==2.1.3
IPython==8.18.1
```

### 6. Add Necessary Files for Resource Downloads

Create a file named `packages.txt` to install system dependencies:
```
build-essential
```

Create a file named `setup.sh` to download NLTK and SpaCy resources:
```bash
#!/bin/bash
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"
python -m spacy download en_core_web_sm
```

Make the file executable:
```bash
chmod +x setup.sh
```

### 7. Adjust Your Code for Hugging Face Environment

Streamlit on Hugging Face Spaces uses different default port settings. Make sure your `app.py` doesn't have hard-coded port configurations.

### 8. Commit and Push Your Code

```bash
git add .
git commit -m "Initial deployment"
git push
```

### 9. Monitor Deployment

1. Go to your Space on Hugging Face (https://huggingface.co/spaces/YOUR_USERNAME/news-analyzer)
2. The deployment will start automatically
3. Check the "Factory Logs" tab to monitor the build process
4. Once completed, your application will be live at the URL provided

### 10. Troubleshooting

If you encounter any issues:

1. Check the logs in the "Factory Logs" tab
2. Ensure all dependencies are correctly specified in `requirements.txt`
3. Verify that path references in your code are relative and not absolute
4. Make sure any temporary files are created in the appropriate directories (use `tempfile` module)

### 11. Update Your Application

To update your deployment after making changes:

```bash
git add .
git commit -m "Update description"
git push
```

The deployment will automatically rebuild with your changes.

## Additional Tips

1. **Environment Variables**: Use Hugging Face's Secret Management if you need to store API keys or other sensitive information.

2. **Persistent Storage**: Spaces doesn't guarantee persistent storage. Use appropriate cloud storage for any data that needs to be persistent.

3. **Resource Limitations**: Be mindful of memory and processing limitations in the free tier. Optimize your code accordingly.

4. **Cache Management**: Use Streamlit's caching mechanisms to improve performance.