from app.dao.basedao import BaseDAO
from app.admin.models import AdminTable


class AdminDAO(BaseDAO):
    model = AdminTable
