from sqlalchemy import ForeignKey
from sqlalchemy.orm import Session

from . import models, schemas


def get_element_or_none(db: Session, item_id: int) -> schemas.Element | None:
    element = (
        db.query(models.Element).filter(models.Element.id == item_id).one_or_none()
    )
    if element is None:
        return element
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
        return element

    element_out = schemas.Element(id=element.id, name=element.name)
    return element_out


# def create_operation(
#     db: Session, new_element: schemas.ElementCreate
# ) -> schemas.Element | None:
#     # get parent option
#     option = (
#         db.query(models.Option)
#         .filter(models.Option.id == new_element.parent)
#         .one_or_none()
#     )
#     if option is None or option.child_element is not None:
#         return None

#     # add the item itself
#     element = models.Element(text=new_element.text)
#     db.add(element)
#     db.commit()
#     db.refresh(element)

#     # connect parent option to new element
#     db.query(models.Option).filter(models.Option.id == new_element.parent).update(
#         {"child_element": element.id}
#     )
#     db.commit()
#     db.refresh(option)

#     # add all of the new options
#     options = [
#         models.Option(parent_element=element.id, text=new_option.text)
#         for new_option in new_element.options
#     ]
#     for option in options:
#         db.add(option)

#     db.commit()

#     element_out = schemas.Element(id=element.id, text=element.text, options=options)
#     return element_out
