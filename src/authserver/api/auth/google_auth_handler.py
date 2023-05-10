from fastapi import APIRouter
from fastapi.responses import RedirectResponse


google_auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@google_auth_router.get("/login/google", response_class=RedirectResponse)
async def login_with_google():
    """
    We will redirect the user to google consent screen for login.
    """
    ...

@google_auth_router.get("/login/google/callback", response_class=RedirectResponse)
async def login_with_google_callback():
    """
    Google Auth Server will make a request here to verify the login.
    After the user verification we will redirect to provide our response token.
    """
    ...