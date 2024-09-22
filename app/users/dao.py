from app.dao.basedao import BaseDAO
from app.users.models import UserTable


class UserDAO(BaseDAO):
    model = UserTable

