# QuizLearn - Educational Quiz Platform with AI-generated Quizzes

**QuizLearn** is an educational web platform that allows users to watch YouTube playlists in the form of courses. As users watch videos, AI-generated quizzes are automatically created based on the content of the videos. Users earn experience points (EXP) and are ranked on a leaderboard. They can also participate in challenges to unlock badges. The backend is built with **FastAPI**, and this repository contains the API that powers the QuizLearn platform.

## Features

- **YouTube Playlist Integration**: Users can watch educational YouTube videos grouped into a playlist.
- **AI-Generated Quizzes**: Based on the video content, AI generates quizzes that test users' knowledge.
- **Experience Points (EXP)**: Users earn EXP by completing quizzes and watching videos.
- **Leaderboard**: Users' rankings are based on their total EXP.
- **Challenges & Badges**: Users can participate in challenges to earn badges for achievements.

## Backend Overview

The backend of the QuizLearn platform is built using **FastAPI** for fast and scalable API development. The platform integrates with various services, including YouTube and AI-based quiz generation, to provide a seamless user experience. The backend also supports user authentication, ranking, and handling quiz data.

## Installation

To set up and run the backend locally, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/quizlearn-backend.git
   cd quizlearn-backend
   
2. Create a virtual environment (optional but recommended):
    ```bash 
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Run the application:
   ```bash
   uvicorn main:app --reload

## Endpoints

Here are some of the key API endpoints exposed by the backend:

POST /register/: Add your username, email id, password, phone number to register
POST /login/: Add your username and password
POST /update_tokens/{user_id}: Updated User's tokens and exp after watching a video and a quiz
GET /users_with_rank/: Retrieve the leaderboard based on users' EXP.
POST /generate_quiz/: AI generated quiz based on the youtube video you just watched.

## Technologies Used

FastAPI: Web framework for building the backend API.
Uvicorn: ASGI server for serving the FastAPI app.
SQLAlchemy: ORM for database interaction.
YouTube Transcript API: Used for extracting transcripts from YouTube videos to generate quizzes.
Requests: For making HTTP requests (e.g., to fetch YouTube data).
Pydantic: For data validation and parsing.
Passlib & Bcrypt: For password hashing and secure authentication.
