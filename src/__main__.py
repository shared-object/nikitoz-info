import asyncio
from . import app
from .settings import load_settings


settings = load_settings()


asyncio.run(app.main(settings))
