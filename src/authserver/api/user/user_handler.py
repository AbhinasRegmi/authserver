from fastapi import APIRouter, Query
from pydantic import EmailStr, AnyHttpUrl

from authserver.schemas.payload_schema import GoogleResponsePayload


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/detail")
def user_detail_from_google(email: EmailStr = Query(...), avatar: AnyHttpUrl = Query(...), verified: bool = Query(...)) -> GoogleResponsePayload:
    """
    This is internal router external apis shouldn't make request directly.
    Authserver will automatically redirect all logins here.

    This route is used by authserver to send the payload data to user. 
    Make sure this path matches the USER_DETAIL_PATH in settings and changes in 
    query params must be propagated to `login_with_google_callback` handler.
    """
    return GoogleResponsePayload(
        email=email,
        avatar=avatar,
        verified=verified
    )