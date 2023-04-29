import motor.motor_asyncio

from app.core.config import settings

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
