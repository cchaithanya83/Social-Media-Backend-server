import datetime as _dt
import pydantic as _pydantic

class _UserBase(_pydantic.BaseModel):
    email: str
 
class UserCreate(_UserBase):
    hashed_password: str
    name: str
 
    class Config:
        orm_mode = True
 
class User(_UserBase):
    id: int
 
    class Config:
        orm_mode = True
        from_orm = True
        from_attributes=True


class Users(_pydantic.BaseModel):
    email: str


class Post(_pydantic.BaseModel):
    email: str
    content: str

    class Config:
        orm_mode = True


