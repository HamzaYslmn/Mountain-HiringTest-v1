# ./routes/OpenAI/stt_service.py

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import base64
import io
import speech_recognition as sr
from middleware.logger_module import logger as log

router = APIRouter(
    prefix="/openai",
    tags=["OpenAI Rest Routes"],
    responses={404: {"description": "Not found"}},
)

async def validate_user(uuid: str):
    if uuid == "public" or uuid is None:
        raise Exception("Unauthorized access")

class STTRequest(BaseModel):
    audio: str
    thread_id: str
    assistant_id: str

@router.post("/stt")
async def stt_rest(request: Request, stt_request: STTRequest):
    await validate_user(request.state.uuid)
    
    try:
        # Decode the base64 audio data
        audio_data = base64.b64decode(stt_request.audio)
        print(f"STT audio data of length: {len(audio_data)}")

        # Use SpeechRecognition to transcribe
        recognizer = sr.Recognizer()
        with sr.AudioFile(io.BytesIO(audio_data)) as source:
            audio = recognizer.record(source)
        transcription = recognizer.recognize_google(audio)

        return {"response": transcription}
    except Exception as e:
        msg = "error in STT Service REST endpoint"
        log.warning(f"{msg} Exception: {e}")
        raise HTTPException(status_code=500, detail=msg)