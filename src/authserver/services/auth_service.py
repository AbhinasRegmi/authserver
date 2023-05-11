from typing import Union, Any, Dict

from pydantic import EmailStr, AnyHttpUrl

from authserver.schemas.token_schema import ResponseToken
from authserver.schemas.payload_schema import GoogleResponsePayload
from authserver.utils.jwt_tokens import generate_access_token, generate_refresh_token, parse_access_token, parse_refresh_token

class TokenService:
    @classmethod
    def get_tokens(cls, payload: Dict[str, Any]) -> ResponseToken:
        """
        Generate access_token and refresh_token
        with the help of payload.
        """
        access_token = generate_access_token(subject=payload)
        refresh_token = generate_refresh_token(subject=payload)

        return ResponseToken(
            access_token=access_token,
            refresh_token=refresh_token
        )

    @classmethod
    def parse_token(cls, token: ResponseToken) -> GoogleResponsePayload:
        """
        Checks if the token is valid with its signature and expire date.
        and returns the valid payload.
        """
        try:
            payload = parse_access_token(token.access_token)
    
            return GoogleResponsePayload(
                email=EmailStr(payload['email']),
                avatar=AnyHttpUrl(url=payload['avatar'], scheme='https'),
                verified=payload['verified']
            )
        except KeyError:
            raise

    @classmethod
    def refresh_token(cls, token: ResponseToken) -> ResponseToken:

        atoken: str = ''
        apayload = cls.parse_token(token)

        if parse_refresh_token(token.refresh_token):
            atoken = generate_access_token(apayload.dict())

        return ResponseToken(
            access_token=atoken,
            refresh_token=token.refresh_token
        )