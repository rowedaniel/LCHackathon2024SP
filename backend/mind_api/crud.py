from sqlalchemy import ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from . import models, schemas


def get_element_or_none(db: Session, item_id: int) -> schemas.Element | None:
    element = (
        db.query(models.Element).filter(models.Element.id == item_id).one_or_none()
    )
    if element is None:
        return None
    element_out = schemas.Element(id=element.id, name=element.name)
    return element_out


def get_random_element(db: Session) -> schemas.Element | None:
    element = db.query(models.Element).order_by(func.random()).first()
    if element is None:
        return None
    element_out = schemas.Element(id=element.id, name=element.name)
    return element_out


def create_element(
    db: Session, new_element: schemas.ElementCreate
) -> schemas.Element | None:
    element = models.Element(name=new_element.name)
    db.add(element)
    db.commit()
    db.refresh(element)
    if element is None:
        return None

    element_out = schemas.Element(id=element.id, name=element.name)
    return element_out


def get_operation_by_parents(
    db: Session, parent_left: int, parent_right: int
) -> schemas.Operation | None:
    operation = (
        db.query(models.Operation)
        .filter(
            models.Operation.parent_left == parent_left
            and models.Operation.parent_right == parent_right
        )
        .one_or_none()
    )
    if operation is None:
        return None
    operation_out = schemas.Operation(**operation.__dict__)
    return operation_out


def create_operation(
    db: Session, new_operation: schemas.OperationCreate
) -> schemas.Operation | None:

    # first check to see that no operation exists of this type
    existing_op = get_operation_by_parents(
        db, new_operation.parent_left, new_operation.parent_right
    )
    if existing_op is not None:
        return None

    # no op exists combining those two elements, so create it
    operation = models.Operation(
        parent_left=new_operation.parent_left,
        parent_right=new_operation.parent_right,
        child=new_operation.child,
    )
    db.add(operation)
    db.commit()
    db.refresh(operation)
    if operation is None:
        return None

    operation_out = schemas.Operation(**operation.__dict__)
    return operation_out
