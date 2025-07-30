from typing import Union

from fastapi import HTTPException, Request
from fastapi.security.base import SecurityBase
from tasteful.authn.user import User


class AuthenticationBackend(SecurityBase):
    def authenticate(self, request: Request) -> Union[User, None]:
        """Authenticate."""
        return None

    async def __call__(self, request: Request) -> None:
        """Callable method."""
        # As this method is supposed to be "Provider Agnostic",
        # it only calls the authenticate method, which returns either an user or None.
        # It then modifies the request to add to it the user value
        try:
            request.state.user = self.authenticate(request=request)
        except Exception:
            raise HTTPException(status_code=500)

        if request.state.user is None:
            raise HTTPException(status_code=401)
