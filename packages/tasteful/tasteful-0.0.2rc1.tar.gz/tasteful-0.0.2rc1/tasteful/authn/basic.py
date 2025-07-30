from typing import Union

from fastapi import Request
from tasteful.authn.authn_backend import AuthenticationBackend
from tasteful.authn.user import User


class BasicAuthenticationBackend(AuthenticationBackend):
    def authenticate(self, request: Request) -> Union[User, None]:
        """Authenticate the user depending on his credentials in the headers."""
        # TODO : switch to body informations
        username = request.headers.get("username")
        password = request.headers.get("password")
        if not username or not password:
            return None
        return self.validate_credentials(username=username, password=password)

    def validate_credentials(self, username: str, password: str) -> Union[User, None]:
        """Return the user info from the backend API."""
        # user = my_api.authenticate(username, password) # noqa: ERA001
        user = User("BasicCredentialsUser")
        return user
