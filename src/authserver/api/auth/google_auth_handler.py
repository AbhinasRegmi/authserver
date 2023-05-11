from fastapi import APIRouter, Query
from pydantic import AnyHttpUrl, EmailStr
from fastapi.responses import RedirectResponse

from authserver.core.config import settings
from authserver.services.auth_service import TokenService
from authserver.schemas.payload_schema import GoogleResponsePayload
from authserver.services.google_service import GoogleServices

google_auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@google_auth_router.get("/login/google", response_class=RedirectResponse)
def login_with_google(referer: AnyHttpUrl = Query(...)):
    """
    We will redirect the user to google consent screen for login.
    """
    return RedirectResponse(url=GoogleServices.get_consent_form_url(referer))
    

@google_auth_router.get("/login/google/callback")
async def login_with_google_callback(code: str = Query(...), state: AnyHttpUrl = Query(...)):
    """
    Google Auth Server will make a request here to verify the login.
    After the user verification we will redirect to provide our response token.
    """
    google_token_response = await GoogleServices.get_access_token_from_google(code)
    user_detail = await GoogleServices.get_user_details_from_google(google_token_response)
    # user_detail = GoogleServices.get_user_detail_from_token(google_token_response)

    response_token = TokenService.get_tokens(user_detail.dict())

    # make sure the query params are correct
    return RedirectResponse(
        url=state + f"?access_token={response_token.access_token}&refresh_token={response_token.refresh_token}&token_type={response_token.token_type}"
    )