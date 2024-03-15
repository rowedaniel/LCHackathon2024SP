from sqlalchemy import ForeignKey
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import func

from . import models, schemas


def create_identity(db: Session) -> schemas.Element | None:
    element = models.Element(name="no thoughts; head empty", order=1)
    db.add(element)
    db.commit()
    db.refresh(element)
    if element is None:
        return None

    element_out = schemas.Element(id=element.id, name=element.name)
    return element_out


def get_identity(db: Session) -> schemas.Element | None:
    return (
        db.query(models.Element)
        .filter(models.Element.order == 1)
        .limit(1)
        .one_or_none()
    )


def get_element_or_none(db: Session, item_id: int) -> schemas.Element | None:
    element = (
        db.query(models.Element)
        .filter(models.Element.id == item_id)
        .limit(1)
        .one_or_none()
    )
    if element is None:
        return None
    element_out = schemas.Element(**element.__dict__)
    return element_out


def get_all_elements(db: Session) -> list[schemas.Element]:
    elements = db.query(models.Element).all()
    return [schemas.Element(**element.__dict__) for element in elements]


def get_all_possible_products(
    db: Session, parent_left: int, parent_right: int
) -> list[schemas.Element]:

    if get_operation_by_parents(db, parent_left, parent_right) is not None:
        return []

    query_bad = (
        db.query(models.Element)
        .join(models.Operation, models.Element.id == models.Operation.child)
        .filter(
            (
                (models.Operation.parent_left == parent_left)
                | (models.Operation.parent_right == parent_right)
            )
        )
    )
    elements = db.query(models.Element).except_(query_bad).all()
    elements_out = [schemas.Element(**element.__dict__) for element in elements]
    return elements_out


def get_random_element(db: Session) -> schemas.Element | None:
    element = db.query(models.Element).order_by(func.random()).first()
    if element is None:
        return None
    element_out = schemas.Element(**element.__dict__)
    return element_out


def create_element(
    db: Session, new_element: schemas.ElementCreate
) -> schemas.Element | None:
    element = models.Element(**new_element.__dict__)
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
            (models.Operation.parent_left == parent_left)
            & (models.Operation.parent_right == parent_right)
        )
        .limit(1)
        .one_or_none()
    )
    if operation is None:
        return None
    operation_out = schemas.Operation(**operation.__dict__)
    return operation_out


def create_operation(
    db: Session, new_operation: schemas.OperationCreate
) -> schemas.Operation | None:

    operation = models.Operation(**new_operation.__dict__)
    db.add(operation)
    db.commit()
    db.refresh(operation)
    if operation is None:
        return None

    operation_out = schemas.Operation(**operation.__dict__)
    return operation_out
