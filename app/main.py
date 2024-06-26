import asyncio
import logging
import time
from contextlib import asynccontextmanager

from fastapi import (APIRouter, Depends, FastAPI, File, HTTPException,
                     UploadFile)
from sqlalchemy.orm import Session

from .crud import create_route, get_route
from .db import check_db_connection, get_db
from .schemas import Route
from .settings import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    check_db_connection()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

router = APIRouter()


@router.post("/routes/", response_model=Route)
async def add_route(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    start_time = time.time()
    try:
        res = await asyncio.to_thread(create_route, db, file)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="Invalid file")
    end_time = time.time()
    file_size_kb = file.size / 1000  # type: ignore

    logger.info(
        f"Processing time of file {file.filename} "
        f"with size {file_size_kb} Kb: {end_time - start_time}"
    )
    return res


@router.get("/routes/{route_id}", response_model=Route)
async def read_route(route_id: int, db: Session = Depends(get_db)):
    return get_route(db, route_id)


app.include_router(router, prefix=settings.API_V1_STR, tags=["routes"])
