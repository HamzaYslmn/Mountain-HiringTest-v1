# ./routes/OpenAI/tts_service.py

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from middleware.logger_module import logger as log
import pyttsx3
import io
import tempfile
import os

router = APIRouter(
    prefix="/openai",
    tags=["OpenAI Rest Routes"],
    responses={404: {"description": "Not found"}},
)

async def validate_user(uuid: str):
    if uuid == "public" or uuid is None:
        raise Exception("Unauthorized access")

class TTSRequest(BaseModel):
    text: str
    thread_id: str
    assistant_id: str

@router.post("/tts")
async def tts_rest(request: Request, tts_request: TTSRequest):
    await validate_user(request.state.uuid)

    try:
        # Use pyttsx3 to synthesize speech to a temporary file
        engine = pyttsx3.init()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tf:
            temp_filename = tf.name
        engine.save_to_file(tts_request.text, temp_filename)
        engine.runAndWait()
        with open(temp_filename, "rb") as f:
            audio_bytes = f.read()
        os.remove(temp_filename)
        return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/wav")
    except Exception as e:
        msg = "error in TTS Service REST endpoint"
        log.warning(f"{msg} Exception: {e}")
        raise HTTPException(status_code=500, detail=msg)