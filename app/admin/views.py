from sqladmin import ModelView

from app.users.models import UserTable
from app.bookings.models import BookingsTable
from app.hotels.models import HotelTable
from app.hotels.rooms.models import RoomTable


class HotelsAdmin(ModelView, model=HotelTable):
    column_list = [column.name for column in HotelTable.__table__.c] + [HotelTable.rooms]
    can_create = True
    can_edit = True
    name = 'Отель'
    name_plural = 'Отели'

    icon = 'fa-solid fa-hotel'


class RoomsAdmin(ModelView, model=RoomTable):
    column_list = [column.name for column in RoomTable.__table__.c] + [RoomTable.hotel, RoomTable.booking]
    can_create = True
    can_edit = True
    name = 'Комната'
    name_plural = 'Комнаты'

    icon = 'fa-solid fa-door-open'


class UserAdmin(ModelView, model=UserTable):
    column_list = [UserTable.id, UserTable.email] + [UserTable.booking]
    column_details_exclude_list = [UserTable.hashed_password]
    can_create = True
    can_delete = False
    can_edit = True
    name = 'Пользователь'
    name_plural = 'Пользователи'
    column_searchable_list = [UserTable.email]
    column_sortable_list = [UserTable.id]

    icon = 'fa-solid fa-user'


class BookingAdmin(ModelView, model=BookingsTable):
    column_list = [column.name for column in BookingsTable.__table__.c] + [BookingsTable.user, BookingsTable.room]
    can_edit = True
    name = 'Бронирование'
    name_plural = 'Бронирования'

    icon = 'fa-solid fa-book'




