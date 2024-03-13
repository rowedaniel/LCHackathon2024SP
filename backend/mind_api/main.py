from typing import Generator

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session

from . import models, schemas
from .crud import create_element, get_element_or_none
from .database import SessionLocal

app = FastAPI(default_response_class=ORJSONResponse)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/getelement", response_model=schemas.Element)
async def get_element(item_id: int, db: Session = Depends(get_db)) -> schemas.Element:
    res = get_element_or_none(db, item_id)
    if res is None:
        raise HTTPException(status_code=404, detail="item not found")
    return res
