from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from authserver.api.router import router_v1
from authserver.core.config import settings


app = FastAPI(
    redoc_url='',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["Home"])
def welcome():
    return {
        "message": "Welcome to AuthServer for abhinasregmi.com.np"
    }


app.include_router(router_v1)