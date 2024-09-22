from app.dao.basedao import BaseDAO
from app.hotels.rooms.models import RoomTable


class RoomDAO(BaseDAO):
    model = RoomTable
