from fastapi import APIRouter

from authserver.schemas.token_schema import ResponseToken
from authserver.schemas.payload_schema import ResponsePayload

token_router = APIRouter(prefix="/auth", tags=["Auth"])


@token_router.get("/get-token", response_model=ResponseToken)
def get_token_after_google_login():
    """
    We will respond with access token and refresh token on successful google login. 
    """
    ...

@token_router.post("/refresh-your-tokens", response_model=ResponseToken)
def refresh_your_tokens():
    """
    After the access_token has been expired. We will use the refesh_token to
    provide new access_token without login.
    """
    ...


@token_router.post("/verify-tokens", response_model=ResponsePayload)
def verify_tokens():
    """
    Authserver will take in access and response token and send the required
    payload if valid.
    """
    ...