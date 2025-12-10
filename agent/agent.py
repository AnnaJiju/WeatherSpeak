# agent/agent.py
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import uuid
from agent.weather import get_weather
from whisper import load_model
from gtts import gTTS

load_dotenv()

app = FastAPI(title="Weather Voice Agent Backend")

# Ensure responses directory exists
RESPONSES_DIR = "responses"
if not os.path.exists(RESPONSES_DIR):
    os.makedirs(RESPONSES_DIR)
    print(f"Created '{RESPONSES_DIR}' directory")

# Allow local frontend origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:9000", "http://localhost:9000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Weather Voice Agent Backend Running"}

@app.get("/weather")
def weather(city: str):
    """
    Query param: city (required)
    Example: /weather?city=Mumbai
    """
    if not city:
        raise HTTPException(status_code=422, detail="Missing 'city' parameter")
    try:
        result = get_weather(city)
        return {"success": True, "city": result.get("city", city), "weather": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather service error: {e}")

@app.post("/process-audio")
async def process_audio(audio: UploadFile = File(...)):
    temp_audio_path = None
    try:
        # Save the uploaded audio file
        temp_audio_path = f"temp_{uuid.uuid4().hex}.wav"
        with open(temp_audio_path, "wb") as f:
            f.write(await audio.read())

        print(f"Saved uploaded audio to: {temp_audio_path}")

        # Transcribe audio using Whisper
        model = load_model("base")
        result = model.transcribe(temp_audio_path)
        text = result["text"]
        print(f"Transcribed text: {text}")

        # Extract location from transcribed text
        location = extract_location(text)
        if not location:
            raise ValueError("No location found in transcribed text. Please mention a city name.")

        # Sanitize location
        sanitized_location = location.rstrip("?.,!")
        print(f"Sanitized location: {sanitized_location}")

        # Fetch weather data
        weather_info = get_weather(sanitized_location)
        print(f"Weather info: {weather_info}")

        weather_text = (
            f"The weather in {weather_info['city']} is {weather_info['description']} "
            f"with a temperature of {weather_info['temp_c']}°C, "
            f"feels like {weather_info['feels_like']}°C, and humidity of {weather_info['humidity']}%."
        )

        # Convert weather info to speech
        tts = gTTS(weather_text)
        
        # Generate unique filename
        audio_filename = f"response_{uuid.uuid4().hex}.mp3"
        audio_response_path = os.path.join(RESPONSES_DIR, audio_filename)
        
        # Save the audio file
        tts.save(audio_response_path)
        print(f"Audio response saved at: {audio_response_path}")

        # Return JSON with the path
        return JSONResponse({
            "success": True,
            "audio_path": f"responses/{audio_filename}",
            "transcribed_text": text,
            "location": sanitized_location,
            "weather_text": weather_text
        })

    except ValueError as e:
        print(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error during processing: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    finally:
        # Clean up temporary audio file
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.remove(temp_audio_path)
                print(f"Cleaned up temp file: {temp_audio_path}")
            except Exception as e:
                print(f"Failed to clean up temp file: {e}")

def extract_location(text):
    """Extract city name from text like 'What's the weather in Mumbai?'"""
    text_lower = text.lower()
    
    # Try "in [city]" pattern
    if " in " in text_lower:
        words = text.split()
        words_lower = text_lower.split()
        try:
            index = words_lower.index("in")
            if index + 1 < len(words):
                return words[index + 1]
        except ValueError:
            pass
    
    # Try "at [city]" pattern
    if " at " in text_lower:
        words = text.split()
        words_lower = text_lower.split()
        try:
            index = words_lower.index("at")
            if index + 1 < len(words):
                return words[index + 1]
        except ValueError:
            pass
    
    # Try "for [city]" pattern
    if " for " in text_lower:
        words = text.split()
        words_lower = text_lower.split()
        try:
            index = words_lower.index("for")
            if index + 1 < len(words):
                return words[index + 1]
        except ValueError:
            pass
    
    return None

# Serve the directory containing audio responses as static files
app.mount("/responses", StaticFiles(directory=RESPONSES_DIR), name="responses")

# Log startup information
print(f"Current working directory: {os.getcwd()}")
print(f"Responses directory: {os.path.abspath(RESPONSES_DIR)}")
print(f"Responses directory exists: {os.path.exists(RESPONSES_DIR)}")