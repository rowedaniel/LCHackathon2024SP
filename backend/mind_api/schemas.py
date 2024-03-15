from pydantic import BaseModel, constr


class ElementBase(BaseModel):
    name: constr(max_length=200)
    order: int|None = None


class ElementCreate(ElementBase):
    pass


class Element(ElementBase):
    id: int

    class Config:
        from_attributes = True


class OperationBase(BaseModel):
    parent_left: int
    parent_right: int
    child: int


class OperationCreate(OperationBase):
    pass


class Operation(OperationBase):
    id: int

    class Config:
        from_attributes = True
