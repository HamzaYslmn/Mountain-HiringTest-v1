from dotenv import load_dotenv
load_dotenv("../../ENV/.env")
load_dotenv("example.env")

from fastapi import FastAPI

# middleware
import middleware.middleware as custom_middleware

# Chat Routes
from routes.AI.chat_route import router as chat_router
from routes.AI.tts_service import router as tts_router
from routes.AI.stt_service import router as stt_router

# Importing routers rest
from routes.root import router as root_router
# from routes.react_FrontEnd import router as react_FrontEnd_router

app = FastAPI(
    title="Mountain API Service",
    description="API service for the MountainAI HireUp360",
    root_path="/AI",
    version="0.0.1",
    redoc_url="/redocs",  # None
    docs_url="/docs"  # None
)

# Add middlewares
custom_middleware.add_middlewares(app)

#* REST routes
# Chat Routes
app.include_router(chat_router)
app.include_router(tts_router)
app.include_router(stt_router)

# Root
app.include_router(root_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)