import logging
import sys
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.endpoint import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)
logging.getLogger("fontTools").setLevel(logging.ERROR)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # init DB/lifespan features
        logger.info("=========================================")
        logger.info("SPEECH BACKEND")
        logger.info(f"VERSION : {settings.APP_VERSION}")
        logger.info(f"ENV : {settings.ENV}" )
        logger.info("DB_HOST : " + settings.DB_HOST)
        logger.info("DB_USER : " + settings.DB_USER)
        logger.info("DB_NAME : " + settings.DB_NAME)
        logger.info("=========================================")
        logger.info("FULL API DOCUMENTATION AT : <API_URL>/docs")
        logger.info("=========================================")

        from sqlalchemy import text
        from db.connection import Engine, SessionLocal

        try:
            from db.connection import Engine, Base
            async with Engine.begin() as conn:
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                # This is the "Safety Net"
                await conn.run_sync(Base.metadata.create_all)
                logger.info("Database schemas verified/created.")
            logger.info("starting up..")
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            raise e
            # sys.exit(1)  # This is

        async with SessionLocal() as db_session:
            try:
                await db_session.execute(text("SELECT 1"))
                print("Database Connection successful !")
            except Exception as e:
                print("FATAL ERROR : Database Connection failed! : \n", e)
        
        yield
    finally:
        print("Shutting down API...")
        await Engine.dispose()

app = FastAPI(openapi_tags=[

    {"name": "crazy-chess",
    "description": "Chesss",
    },
    ],lifespan=lifespan, title="Crazy Chess API")

app.include_router(router)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    ]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])



@app.get("/health")
async def health_check():
    return {"status": "OK"}