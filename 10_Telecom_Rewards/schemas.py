from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str
    number: int

class Recharge(BaseModel):
    user_id: int
    amount: int

class Redeem(BaseModel):
    user_id: int
    points: int

