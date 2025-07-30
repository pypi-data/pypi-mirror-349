from typing import Union

from fastapi import Request
from tasteful.authn.authn_backend import AuthenticationBackend
from tasteful.authn.user import User


class OIDCAuthenticationBackend(AuthenticationBackend):
    def authenticate(self, request: Request) -> Union[User, None]:
        """Authenticate the user depending on the token in the request headers."""
        authorization = request.headers.get("Authorization")
        if not authorization:
            return None
        else:
            token = authorization.split(" ")[1]

            # This method calls the OIDC Backend (zitadel for example)
            # to authenticate the user
            return self.validate_token(token)

    def validate_token(self, token: str) -> Union[User, None]:
        """Return the user info from the backend API."""
        # user = my_api.authenticate(token) # noqa: ERA001
        user = User("OIDCUser")
        return user
