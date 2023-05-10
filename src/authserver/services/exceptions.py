from fastapi import HTTPException, status

class InvalidAccessTokenGoogleError(HTTPException):
    def __init__(self):
        return super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please try logging in again."
        )