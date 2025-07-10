from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
import json
import asyncio
import base64
from typing import AsyncGenerator

from middleware.logger_module import logger as log

router = APIRouter(
    prefix="/openai",
    tags=["OpenAI Rest Routes"],
    responses={404: {"description": "Not found"}},
)

async def validate_user(uuid: str):
    if uuid == "public" or uuid is None:
        raise Exception("Unauthorized access")

async def chunkify(data: str, size: int = 3, pause: float = 0.1) -> AsyncGenerator[bytes, None]:
    encoded = data.encode("utf-8")
    for i in range(0, len(encoded), size):
        yield encoded[i : i + size]
        await asyncio.sleep(pause)

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message to AI")
    agent_id: Optional[str] = Field("pmpt_6867eb8b4fc08195929708cbd183ca420d2cf33d36b5ace3", description="ID of the AI agent to use")
    photo: Optional[str] = Field(None, description="Base64 encoded image data or URL of the image")
    response_id: Optional[str] = Field(None, description="Previous response ID")
    
    model_config = ConfigDict(extra="ignore")

@router.post("/chat")
async def chat_endpoint(request: Request, body: ChatRequest) -> StreamingResponse:
    # 1) --- authorisation ---------------------------------------------------
    token = getattr(request.state, "uuid", None) or request.headers.get("Authorization")
    await validate_user(token)

    # 2) --- optional photo validation --------------------------------------
    if body.photo:
        if body.photo.startswith("http"):
            pass  # URL is OK
        elif body.photo.startswith("data:image/"):
            base64.b64decode(body.photo.split(",", 1)[1], validate=True)
        else:
            raise HTTPException(400, "photo must be a URL or base-64 string")

    # 3) --- craft the reply -------------------------------------------------
    response_id = "resp_123"
    output = {
        "emotion": "curious",
        "output": (
            "Merhaba! Ben Mountain Yapay Zeka. Projelerimiz, teknolojilerimiz "
            "ve ekibimiz hakkında size yardımcı olabilirim. Sizi en çok hangi "
            "konular ilgilendiriyor?"
        ),
    }
    
    payload = json.dumps(output, ensure_ascii=False)

    # 4) --- stream the JSON chunks -----------------------------------------
    return StreamingResponse(chunkify(payload), media_type="application/json")