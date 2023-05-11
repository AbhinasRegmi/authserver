import httpx
from jose import jwt
from pydantic import EmailStr, AnyHttpUrl

from authserver.core.config import settings
from authserver.schemas.token_schema import GoogleResponseToken
from authserver.schemas.payload_schema import GoogleResponsePayload
from authserver.services.exceptions import InvalidAccessTokenGoogleError


class GoogleServices:
    @classmethod
    def get_consent_form_url(cls) -> str:
        """
        Build the required  request with appropriate scopes and parameters to show
        consent screen to the end user. It will return the url of consent form.
        """
        HEADERS = {"Accept": "application/json"}
        params = {
            "redirect_uri": settings.AUTHSERVER_GOOGLE_CALLBACK_URL,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "access_type": "offline",
            "response_type": "code",
            "prompt": "consent",
            "scope": " ".join(
                [
                    settings.GOOGLE_PROFILE_SCOPE_URL,
                    settings.GOOGLE_EMAIL_SCOPE_URL
                ]
            )
        }

        consent_url = httpx.Client().build_request(method="GET", url=settings.GOOGLE_OAUTH_ROOT_URL, headers=HEADERS, params=params).url

        return str(consent_url)
    

    @classmethod
    async def get_access_token_from_google(cls, code: str) -> GoogleResponseToken:
        """
        Using the code that is obtained after login from consent screen we will
        request google to provide us with access_token to login as that user.
        """
        HEADERS = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        params = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.AUTHSERVER_GOOGLE_CALLBACK_URL,
            "grant_type": "authorization_code"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url=settings.GOOGLE_OAUTH_TOKEN_URL, headers=HEADERS, params=params)

            response_json = response.json()

            return GoogleResponseToken(
                access_token=response_json['access_token'],
                id_token=response_json['id_token']
            )
        
        except KeyError:
            raise InvalidAccessTokenGoogleError
        
    @classmethod
    def get_user_detail_from_token(cls, token: GoogleResponseToken) -> GoogleResponsePayload:
        """
        We can obtain the email and profile directly from id_token.
        But cannot verify the signature of the jwt_token.
        """

        google_payload = jwt.get_unverified_claims(token.id_token)

        return GoogleResponsePayload(
            username='-',
            email=EmailStr(google_payload['email']),
            avatar=AnyHttpUrl(url=google_payload['picture'], scheme="https")
        )
    
        
    @classmethod
    async def get_user_details_from_google(cls, token: GoogleResponseToken) -> GoogleResponsePayload:
        """
        We will use access_token and token_id to login as external user and connect
        with googleapis to extract user data like email, avatar_url and validity of
        google account.
        """

        header = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token.id_token}"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url=settings.GOOGLE_API_USERINFO_URL+token.access_token, headers=header)

            response_json = response.json()

            return GoogleResponsePayload(
                username=response_json['name'],
                email=EmailStr(response_json['email']),
                avatar=AnyHttpUrl(response_json['picture'], scheme='https'),
                verified=response_json['verified_email']
            )

        except KeyError:
            raise InvalidAccessTokenGoogleError