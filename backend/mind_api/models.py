from sqlalchemy import Column, Date, ForeignKey, Integer, String

from .database import Base


class Element(Base):
    __tablename__ = "elements"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200))
    order = Column(Integer)


class Operation(Base):
    __tablename__ = "operations"
    id = Column(Integer, primary_key=True, index=True)
    parent_left = Column(Integer, ForeignKey("elements.id"), nullable=False)
    parent_right = Column(Integer, ForeignKey("elements.id"), nullable=False)
    child = Column(Integer, ForeignKey("elements.id"), nullable=False)
