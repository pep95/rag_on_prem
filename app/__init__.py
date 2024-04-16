from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.api_settings import get_api_settings

from config import Settings
from app.views import router

settings = Settings()
get_api_settings.cache_clear()
app_settings = get_api_settings()

if settings.ENV == "dev":
    app_settings.debug = True
else:
    app_settings.debug = False

app = FastAPI(**app_settings.fastapi_kwargs)

origins = [""]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.router)
