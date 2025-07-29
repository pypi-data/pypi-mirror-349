from typing import Union

from fastapi import Request
from tasteful.authn.authn_backend import AuthenticationBackend
from tasteful.authn.user import User


class ApiKeyAuthenticationBackend(AuthenticationBackend):
    def authenticate(self, request: Request) -> Union[User, None]:
        """Authenticate the user depending on his api key in the headers."""
        key = request.headers.get("api_key")
        if not key:
            return None
        else:
            return self.validate_credentials(key=key)

    def validate_credentials(self, key: str) -> Union[User, None]:
        """Return the user info from the backend API."""
        # user = my_api.authenticate(key)  # noqa: ERA001
        user = User("ApiKeyCredentialsUser")
        return user
