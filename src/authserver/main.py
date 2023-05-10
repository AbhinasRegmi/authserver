from fastapi import FastAPI

from authserver.api.router import router_v1

app = FastAPI(
    redoc_url='',
)


@app.get("/", tags=["Home"])
def welcome():
    return {
        "message": "Welcome to AuthServer for abhinasregmi.com.np"
    }


app.include_router(router_v1)