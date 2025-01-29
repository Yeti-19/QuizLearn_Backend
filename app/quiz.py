import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Define request model
class VideoRequest(BaseModel):
    video_id: str

# Function to fetch the YouTube transcript using YouTube video ID
def get_youtube_transcript(video_id):
    try:
        # Fetch the transcript from YouTube using the video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Optional: format the transcript into JSON (if you need to format it)
        formatter = JSONFormatter()
        formatted_transcript = formatter.format_transcript(transcript)

        return json.loads(formatted_transcript)
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return []

# Function to generate quiz questions from the YouTube transcript using Perplexity API
def generate_quiz_from_transcript(transcript):
    # Perplexity API endpoint
    url = "https://api.perplexity.ai/chat/completions"

    # API payload for generating quiz questions based on the transcript content
    payload = {
        "model": "sonar",  # Model to be used for generating quiz
        "messages": [
            {
                "role": "system",
                "content": "Generate 10 multiple-choice quiz questions with 4 short options each, and provide the correct answer for each question, based on the following text."
            },
            {
                "role": "user",
                "content": "\n".join([entry['text'] for entry in transcript])  # Extract text from each transcript entry
            }
        ],
        "max_tokens": 800,  # Further increase token limit for more detailed responses
        "temperature": 0.5,  # Adjust randomness of responses
        "top_p": 0.9,
        "search_domain_filter": ["perplexity.ai"],
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": "month",
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1,
    }

    # Headers with API token
    headers = {
        "Authorization": "Bearer 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",  # Replace with your actual API token
        "Content-Type": "application/json"
    }

    try:
        # Send POST request to Perplexity API
        response = requests.post(url, json=payload, headers=headers)

        # Check if the response is successful (status code 200)
        if response.status_code == 200:
            response_data = response.json()
            quiz = response_data.get('choices', [])
            if quiz:
                return quiz[0].get('message', {}).get('content', '')
            else:
                return "No quiz questions generated."
        elif response.status_code == 401:
            return "Error: Unauthorized - Check your API Key."
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

