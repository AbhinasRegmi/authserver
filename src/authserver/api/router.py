from fastapi import APIRouter

from authserver.api.user.user_handler import user_router
from authserver.api.mail.mail_handler import mail_router
from authserver.api.auth.google_auth_handler import google_auth_router
from authserver.api.auth.token_handler import token_router

router_v1 = APIRouter(prefix="/api/v1")

router_v1.include_router(user_router)
router_v1.include_router(google_auth_router)
router_v1.include_router(token_router)
router_v1.include_router(mail_router)