from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form, Depends
from fastapi.responses import StreamingResponse, HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
from dotenv import load_dotenv
import asyncio
import speech_recognition as sr
import pyttsx3
import io

# Import your services
from ChatGPT.xChat_gpt import process_user_input

app = FastAPI()

# CORS Middleware (for preflight requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jinja2 Templates
templates = Jinja2Templates(directory="static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# AI Services -------------------------------------------------------------------------------------------------------------------------------------------------

@app.post("/chatbot/")  
async def process_user_input_stream(userinput: str = Form(...),
                                    thread_id: str = Form(...),
                                    assistant_id: str = Form(...),
                                    username: str = Form(...)
                                    ):
    response = []
    print(f"Received user input: {userinput}")
    print(f"Received thread id: {thread_id}")
    print(f"Received assistant id: {assistant_id}")
    print(f"Received username: {username}")
    
    if "ERR!" in userinput:
        raise HTTPException(status_code=400, detail="Error")
    
    async for assistant_response, thread_id, message_time, error in process_user_input(userinput, thread_id, assistant_id):
        if error:
            raise HTTPException(status_code=500, detail=error)
        response.append({
            "assistant_response": assistant_response,
            "thread_id": str(thread_id),
            "message_time": message_time.isoformat()
        })
    
    return response




@app.post("/vision/")
async def process_vision(
    userinput: str = Form(...),
    thread_id: str = Form(...),
    assistant_id: str = Form(...),
    image_file: UploadFile = File(...)
):
    # Validate image file
    valid_extensions = {".jpg", ".jpeg", ".png"}
    file_extension = os.path.splitext(image_file.filename)[-1].lower()
    
    if file_extension not in valid_extensions:
        raise HTTPException(status_code=400, detail="Invalid image file extension. Only JPG, JPEG, or PNG files are accepted.")
    
    image_data = await image_file.read()
    if len(image_data) == 0:
        raise HTTPException(status_code=400, detail="Empty image file.")

    # Process the image (placeholder, add your processing logic here)
    content = "This file is okay."
    new_thread_id = thread_id

    # Simulate a response
    return {"VisionOutput": content, "thread_id": new_thread_id}


async def local_tts_service(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set properties before speaking
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

    # Speak the given text
    engine.say(text)
    engine.runAndWait()

    print("TTS processing complete")
    
@app.post("/tts/")
async def process_tts(request: dict):
    user_input = request.get("user_input")
    if not user_input:
        raise HTTPException(status_code=400, detail="No text provided for TTS")

    # Process TTS and return as a complete response
    audio_stream = io.BytesIO()
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)

    # Save the TTS output as a WAV file in the BytesIO stream
    engine.save_to_file(user_input, 'output.wav')
    engine.runAndWait()

    # Read the WAV file and return it as a response
    with open('output.wav', 'rb') as f:
        audio_stream = io.BytesIO(f.read())

    # Ensure the stream is at the beginning before sending it
    audio_stream.seek(0)

    # Return the audio stream as a WAV file
    return StreamingResponse(audio_stream, media_type="audio/wav")



@app.post("/stt/")
async def process_stt(thread_id: str = Form(...), assistant_id: str = Form(...), audio_file: UploadFile = File(...)):
    audio_data = await audio_file.read()
    print(f"Received audio data of length: {len(audio_data)}")
    if len(audio_data) == 0:
        return {"stt_response": "No audio data received, please check the microphone and try again. ERR!"}

    # Use BytesIO to create a file-like object from the audio data
    audio_file_like = io.BytesIO(audio_data)

    try:
        transcription = await local_stt_service(audio_file_like)
        return {"stt_response": str(transcription)}

    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"stt_response": "Sound data received but: " + str(e)}

async def local_stt_service(audio_file_like):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file_like) as source:
        audio = recognizer.record(source)  # Record the audio from the file
    transcription = recognizer.recognize_google(audio)
    return transcription

# Web Pages ---------------------------------------------------------------------------------------------------------------------------------------------------
@app.get("/HR")
async def get_home(request: Request):
    return templates.TemplateResponse("recruiter/recruiter.html", {"request": request})

@app.get("/")
async def get_home(request: Request):
    response = {"status":"online",
                "output":"Welcome to the Mountain API Service! 🏔️",
                "🌌":"Or perhaps you're looking for the answer to the ultimate question of life, the universe, and everything?"}
    return response



if __name__ == '__main__':
    import uvicorn
    print("\n\n http://localhost:8000/HR \n\n")
    uvicorn.run("xMain:app", host="0.0.0.0", port=8000, reload=True)