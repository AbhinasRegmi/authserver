from fastapi import APIRouter


mail_router = APIRouter(prefix="/mail", tags=["Mail"])

@mail_router.get("/")
def mail_hello():
    return {
        "message": "This is mail router."
    }