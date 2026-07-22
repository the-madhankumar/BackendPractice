from pydantic import BaseModel, EmailStr

class CreateFamily(BaseModel):
    family_name: str
    primary_name: str

class AddMember(BaseModel):
    name: str


class User(BaseModel):
    id: int
    name: str
    is_primary: bool


class Family(BaseModel):
    id: int
    name: str
    users: list[User]