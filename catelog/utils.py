import os
import requests
from django.conf import settings
import json

def generate_book_summary(title):
    """
    Generate a book summary using OpenAI API based on the book title.
    
    Args:
        title (str): The book title
        
    Returns:
        str: Generated summary or error message
    """
    try:
        # Get API key from settings
        api_key = settings.OPENAI_API_KEY
        
        if api_key == 'your-openai-api-key-here':
            return "Please configure your OpenAI API key in settings.py"
        
        # OpenAI API endpoint
        url = "https://api.openai.com/v1/chat/completions"
        
        # Headers for the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Prompt for generating book summary
        prompt = f"""Based on the book title "{title}", generate a brief, engaging summary (2-3 sentences) that could be used in a library catalog. 
        The summary should be informative and appealing to potential readers. 
        If the title is generic or unclear, make a reasonable assumption about the book's content."""
        
        # Request payload
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        # Make the API request
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            summary = result['choices'][0]['message']['content'].strip()
            return summary
        else:
            return f"Error: Unable to generate summary. Status code: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return "Error: Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error: Network error - {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}" 