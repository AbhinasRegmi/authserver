from fastapi import APIRouter, Body

from authserver.schemas.token_schema import ResponseToken
from authserver.services.auth_service import TokenService
from authserver.schemas.payload_schema import GoogleResponsePayload

token_router = APIRouter(prefix="/auth", tags=["Auth"])


@token_router.post("/refresh-your-tokens", response_model=ResponseToken)
def refresh_your_tokens(token: ResponseToken = Body(...)):
    """
    After the access_token has been expired. We will use the refesh_token to
    provide new access_token without login.
    """
    response_token = TokenService.refresh_token(token)

    return response_token


@token_router.post("/verify-tokens", response_model=GoogleResponsePayload)
def verify_tokens(token: ResponseToken = Body(...)):
    """
    Authserver will take in access and response token and send the required
    payload if valid.
    """
    payload = TokenService.parse_token(token)

    return payload