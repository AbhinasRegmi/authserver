from fastapi import HTTPException, status

class InvalidAccessToken(HTTPException):
    def __init__(self) -> None:
        return super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access_token")
    
class InvalidRefreshToken(HTTPException):
    def __init__(self) -> None:
        return super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh_token")
    
class AccessTokenExpired(HTTPException):
    def __init__(self) -> None:
        return super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your access_token has expired.")
    
class RefreshTokenExpired(HTTPException):
    def __init__(self) -> None:
        return super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your refresh_token has expired.")