from fastapi import APIRouter, Query
from pydantic import AnyHttpUrl
from fastapi.responses import RedirectResponse

from authserver.services.google_service import GoogleServices
from authserver.core.config import settings

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


    # make sure the query params are correct
    return RedirectResponse(
        url=settings.AUTHSERVER_USER_DETAIL_PATH
        + f"?username={user_detail.username}&email={user_detail.email}&avatar={user_detail.avatar}&verified={user_detail.verified}"
    )