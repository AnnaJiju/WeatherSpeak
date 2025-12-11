🌤️## WeatherSpeak- A weather voice agent

A real-time voice-powered weather application that lets you ask about weather conditions in any city using natural speech. Simply speak your question, and get instant audio responses!


✨## Features

🎙️ Voice Recognition - Speak naturally using OpenAI Whisper for accurate transcription

🌍 Real-time Weather - Get current weather data from OpenWeatherMap API

🔊 Voice Response - Hear weather details with natural text-to-speech

🎨 Beautiful UI - Clean, modern interface with gradient backgrounds

⚡ Fast Processing - Quick transcription and response generation

🔒 Privacy Focused - All processing happens locally, no data stored


🎬## Demo
How to Use:

Click "Start Recording"

Speak your question: "What's the weather in Mumbai?"

Wait 5 seconds for recording to complete

Get instant voice response with weather details!


Supported Question Patterns:

"What's the weather in [city]?"

"Tell me the weather at [city]"

"How's the weather for [city]?"


🛠️## Tech Stack
##Frontend

HTML5 - Structure and layout

CSS3 - Styling with modern gradients

JavaScript (Vanilla) - No frameworks needed

MediaRecorder API - Browser audio capture


##Backend

FastAPI - Modern Python web framework

OpenAI Whisper - State-of-the-art speech recognition

gTTS - Google Text-to-Speech engine

OpenWeatherMap API - Comprehensive weather data


##Python Libraries
fastapi          # Web framework

uvicorn          # ASGI server

whisper          # Speech-to-text

gtts             # Text-to-speech

requests         # HTTP client

python-dotenv    # Environment management

##📋 Prerequisites

Before you begin, ensure you have:

Python 3.8 or higher - Download here

pip - Python package installer (comes with Python)

OpenWeatherMap API Key - Get free API key


##🚀 Installation
1. Clone the Repository
   
bashgit clone https://github.com/yourusername/weather-voice-agent.git

cd weather-voice-agent

3. Create Virtual Environment
   
Windows:

bashpython -m venv venv

venv\Scripts\activate

Mac/Linux:

bashpython3 -m venv venv

source venv/bin/activate

5. Install Dependencies
   
bashpip install -r requirements.txt

This will install:


FastAPI and Uvicorn

OpenAI Whisper

Google Text-to-Speech (gTTS)

Other required packages


4. Set Up Environment Variables
   
Create a .env file in the project root:

envOPENWEATHER_API_KEY=your_api_key_here

Get your API key:


Go to OpenWeatherMap

Sign up for a free account

Navigate to API Keys section

Copy your API key


5. Create Responses Directory
   
bashmkdir responses

##💻 Usage

Start the Application

Terminal 1 - Backend Server:

bashpython -m uvicorn agent.agent:app --reload --port 8000

You should see:

INFO:     Uvicorn running on http://127.0.0.1:8000

Created 'responses' directory

INFO:     Application startup complete.

Terminal 2 - Frontend Server:

bashcd frontend

python -m http.server 9000

You should see:

Serving HTTP on :: port 9000 (http://[::]:9000/) ...

Access the Application

Open your browser and navigate to:

http://localhost:9000

Using the Voice Agent


Click the green "Start Recording" button

Speak your weather question clearly (you have 5 seconds)

Wait for processing (transcription → weather fetch → speech generation)

Listen to the voice response with complete weather details

