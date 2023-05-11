from typing import Optional, Union, Any, Dict
from datetime import datetime, timedelta

from jose import jwt, JWTError

from authserver.core.config import settings
from authserver.utils.exceptions import InvalidAccessToken, AccessTokenExpired, InvalidRefreshToken, RefreshTokenExpired


def generate_access_token(subject: Dict[str, Any], expires_minutes: Optional[int] = None) -> str:
    """
    Takes subject like id or email with optional timedelta
    The default expiration date is 15 minutes. Be careful that
    the subject must be JSONable .
    """

    if expires_minutes:
        expires = datetime.utcnow() + timedelta(minutes=expires_minutes)
    else:
        expires = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION)

    to_encode = {"expire": expires, "sub": subject}

    access_token = jwt.encode(to_encode, key=settings.JWT_ACCESS_SECRET, algorithm=settings.JWT_ALGORITHM)

    return access_token


def generate_refresh_token(subject: Dict[str, Any], expires_minutes: Optional[int] = None) -> str:
    """
        Takes subject like id or email with optional timedelta as integer
        The default expiration date is 7 days. Be careful that
        the subject must be JSONable .
    """

    if expires_minutes:
        expires = datetime.utcnow() + timedelta(minutes=expires_minutes)
    else:
        expires = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRATION)

    to_encode = {"expire": expires, "sub": subject}

    refresh_token = jwt.encode(to_encode, key=settings.JWT_REFRESH_SECRET, algorithm=settings.JWT_ALGORITHM)

    return refresh_token


def parse_access_token(token: str) -> Dict[str, Any]:
    """
    Returns `sub` from the payload.
    """
    try:
        payload = jwt.decode(token, key=settings.JWT_ACCESS_SECRET, algorithms=[settings.JWT_ALGORITHM])
    
        if (datetime.fromtimestamp(payload['expire']) < datetime.utcnow()):
            raise AccessTokenExpired
        
        subject = payload['sub']
        
        return subject
    
    except (JWTError, KeyError):
        raise InvalidAccessToken

def parse_refresh_token(token: str) -> Dict[str, Any]:
    """
    Returns `sub` from the payload.
    """
    try:
        payload = jwt.decode(token, key=settings.JWT_REFRESH_SECRET, algorithms=[settings.JWT_ALGORITHM])

        if (datetime.fromtimestamp(payload['expire']) < datetime.utcnow()):
            raise RefreshTokenExpired
        
        subject = payload['sub']

        return subject
    
    except (JWTError, KeyError):
        raise InvalidRefreshToken


