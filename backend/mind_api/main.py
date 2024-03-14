from typing import Generator

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session

from . import models, schemas
from .crud import (create_element, create_operation, get_element_or_none,
                   get_operation_by_parents, get_random_element)
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


@app.get("/element/id", response_model=schemas.Element)
async def get_element(item_id: int, db: Session = Depends(get_db)) -> schemas.Element:
    res = get_element_or_none(db, item_id)
    if res is None:
        raise HTTPException(
            status_code=404, detail="no element with corresponding id found"
        )
    return res


@app.get("/element/random", response_model=schemas.Element)
async def get_rand_elem(db: Session = Depends(get_db)) -> schemas.Element:
    res = get_random_element(db)
    if res is None:
        raise HTTPException(status_code=404, detail="no element found")
    return res


@app.post("/element/create", response_model=schemas.Element)
async def create_elem(
    element: schemas.ElementCreate, db: Session = Depends(get_db)
) -> schemas.Element:
    res = create_element(db, element)
    if res is None:
        raise HTTPException(status_code=404, detail="failed to create item")
    return res


@app.get("/operation/fromparents", response_model=schemas.Operation)
async def get_operation(
    parent_left: int, parent_right: int, db: Session = Depends(get_db)
) -> schemas.Operation:
    res = get_operation_by_parents(db, parent_left, parent_right)
    if res is None:
        raise HTTPException(
            status_code=404, detail="no operation with corresponding parent ids found"
        )
    return res


@app.post("/operation/create", response_model=schemas.Operation)
async def create_elem(
    operation: schemas.OperationCreate, db: Session = Depends(get_db)
) -> schemas.Operation:
    res = create_operation(db, operation)
    if res is None:
        raise HTTPException(
            status_code=404,
            detail="failed to create operation (perhaps it already existed?)",
        )
    return res
