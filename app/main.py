from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingAdmin, HotelsAdmin, RoomsAdmin, UserAdmin
from app.bookings.router import router as booking_router
from app.database import engine
from app.hotels.rooms.router import router as room_router
from app.hotels.router import router as hotel_router
from app.images.router import router as images_router
from app.pages.router import router as pages_router
from app.users.router import router as user_router

from app.logger import logger

from app.settings import settings

from fastapi_versioning import VersionedFastAPI


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"{settings.REDIS_HOST}://localhost:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache:")
    yield


app = FastAPI(debug=True,
              title='Бронирование API',
              summary='Бронирование комнат',
              description='Бронирование комнат в отелях, API',
              version='0.0.1',
              lifespan=lifespan
              )


app.include_router(user_router)
app.include_router(booking_router)
app.include_router(hotel_router)
app.include_router(pages_router)
app.include_router(images_router)

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=['Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers', 'Access-Authorization'],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info('Request handling time:', extra={'process_time': round(process_time, 2)})
    return response

app = VersionedFastAPI(app,
                       version_format='{major}',
                       prefix_format='/v{major}')

app.mount('/static', StaticFiles(directory='app/static'), 'static')

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)