from datetime import timedelta

from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.exceptions import IncorrectEmailException, IncorrectPasswordException
from app.users.auth import verify_password, create_access_token
from app.users.dao import UserDAO
from app.admin.dao import AdminDAO

from app.users.dependencies import get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        user = await UserDAO.find_one_or_none(email=username)
        if user:
            access_token = create_access_token({'sub': str(user.id)}, expires_delta=timedelta(minutes=15))
            request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        user = await get_current_user(token)

        if not user:
            return False

        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key="...")

