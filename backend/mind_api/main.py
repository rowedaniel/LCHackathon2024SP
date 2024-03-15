from typing import Generator

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session

from .crud import (create_element, create_identity, create_operation,
                   get_all_elements, get_all_possible_products,
                   get_element_or_none, get_identity, get_operation_by_parents,
                   get_random_element)
from .database import SessionLocal
from .schemas import Element, ElementCreate, Operation, OperationCreate
from .sudoku_solve import construct_table, verify_table_options

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


@app.get("/element/id", response_model=Element)
async def get_elem(item_id: int, db: Session = Depends(get_db)) -> Element:
    res = get_element_or_none(db, item_id)
    if res is None:
        raise HTTPException(
            status_code=404, detail="no element with corresponding id found"
        )
    return res


@app.get("/element/allpossible")
async def get_possible_elems(
    parent_left: int, parent_right: int, db: Session = Depends(get_db)
) -> list[Element]:
    res = get_all_possible_products(db, parent_left, parent_right)
    if len(res) == 0:
        return []

    # refine by sudoku
    elements = get_all_elements(db)
    table = construct_table(db, elements)
    options, _ = verify_table_options(db, table, elements, parent_left, parent_right)
    return [elements[o] for o in options]


@app.get("/element/all")
async def get_elems(db: Session = Depends(get_db)) -> list[Element]:
    res = get_all_elements(db)
    return res


@app.get("/element/random", response_model=Element)
async def get_rand_elem(db: Session = Depends(get_db)) -> Element:
    res = get_random_element(db)
    if res is None:
        raise HTTPException(status_code=404, detail="no element found")
    return res


@app.post("/element/create_identity")
async def create_e(db: Session = Depends(get_db)) -> tuple[Element, Operation]:
    if get_identity(db) is not None:
        raise HTTPException(status_code=404, detail="identity already created")

    res = create_identity(db)
    if res is None:
        raise HTTPException(status_code=404, detail="error creating identity")
    op = create_operation(
        db, OperationCreate(parent_left=res.id, parent_right=res.id, child=res.id)
    )
    return res, op


@app.post("/element/create")
async def create_elem(
    element: ElementCreate, db: Session = Depends(get_db)
) -> tuple[Element, Operation|None, Operation|None]:
    identity = get_identity(db)
    if identity is None:
        raise HTTPException(status_code=404, detail="identity not created")
    res = create_element(db, element)
    if res is None:
        raise HTTPException(status_code=404, detail="failed to create item")

    # create left and right operations with identity
    left = create_operation(
        db, OperationCreate(parent_left=res.id, parent_right=identity.id, child=res.id)
    )
    right = create_operation(
        db, OperationCreate(parent_left=identity.id, parent_right=res.id, child=res.id)
    )
    return res, left, right


@app.get("/operation/fromparents", response_model=Operation)
async def get_op(
    parent_left: int, parent_right: int, db: Session = Depends(get_db)
) -> Operation:
    res = get_operation_by_parents(db, parent_left, parent_right)
    if res is None:
        raise HTTPException(
            status_code=404, detail="no operation with corresponding parent ids found"
        )
    return res


@app.post("/operation/create")
async def create_op(
    operation: OperationCreate, db: Session = Depends(get_db)
) -> list[Operation]:

    # check that everything exists
    # TODO: there has got to be a better way of doing this
    if (
        get_element_or_none(db, operation.parent_left) is None
        or get_element_or_none(db, operation.parent_right) is None
        or get_element_or_none(db, operation.child) is None
    ):
        raise HTTPException(
            status_code=404,
            detail="needed element(s) doesn't exist",
        )

    # first check to see that no operation exists of this type
    existing_op = get_operation_by_parents(
        db, operation.parent_left, operation.parent_right
    )
    if existing_op is not None:
        raise HTTPException(
            status_code=404,
            detail="operation already existed",
        )

    # refine by sudoku
    elements = get_all_elements(db)
    table = construct_table(db, elements)
    options, tables = verify_table_options(
        db, table, elements, operation.parent_left, operation.parent_right
    )

    # make sure this choice actually works
    id_options = [elements[o].id for o in options]
    if operation.child not in id_options:
        raise HTTPException(
            status_code=404,
            detail="failed to create operation due to group rules",
        )

    # no op exists combining those two elements, so create it
    res = []
    # now create all the other necessary ops for this to work
    selected_i = id_options.index(operation.child)
    selected_table = tables[selected_i]
    for row, left in enumerate(elements):
        for col, right in enumerate(elements):
            print(row, col, table[row][col])
            if len(selected_table[row][col]) != 1 or len(table[row][col]) == 1:
                continue
            create_op = OperationCreate( parent_left=left.id, parent_right=right.id, child=operation.child)

            # make sure op doesn't exist
            existing_op = get_operation_by_parents(
                db, left.id, right.id
            )
            if existing_op is not None:
                continue

            # doesn't exist, so create it
            op = create_operation(
                db,
                create_op
            )
            if op is None:
                raise HTTPException(
                    status_code=404,
                    detail="failed to create operation",
                )
            res.append(op)

    return res
