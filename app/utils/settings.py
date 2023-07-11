import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB = os.getenv(
        "DATABASE_URL",
    )
    TEST_DB = os.getenv(
        "TEST_DATABASE"
    )
    SECRET = os.getenv("SECRET_KEY")
    REDIS_HOST = os.getenv("REDIS_HOST")


settings = Settings()

