import asyncio
import time
import sentry_sdk
from contextlib import asynccontextmanager
from datetime import date
from typing import Optional


from fastapi import Depends, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from pydantic import BaseModel
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView
from prometheus_fastapi_instrumentator import Instrumentator, metrics


from app.admin.auth import authentication_backend
from app.admin.view import BookingsAdmin, HotelsAdmin, RoomsAdmin, UserAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.Users.router import router_auth as router_users
from app.importer.importer import router as router_tables
from app.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.REDIS_DATA)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


from fastapi import FastAPI
import sentry_sdk

sentry_sdk.init(
    dsn="https://c8bdd9d5b8cbdad39f4a616ea864038d@o4506705256579072.ingest.sentry.io/4506705280434176",

    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


app = FastAPI(lifespan=lifespan) 




app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)
app.include_router(router_tables)



origins =[
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=['GET', "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=['Content-Type', "Set-Cookie", "Access-Control-Allow-Headers", "Acces-Control-Allow-Origin", "Autorization"]
)


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)



instrumentator = Instrumentator(
should_group_status_codes=False,
 excluded_handlers=[".*admin.*", "/metrics"],
)

instrumentator.instrument(app).expose(app)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response