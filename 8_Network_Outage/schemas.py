from pydantic import BaseModel
from enum import Enum

class Status(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    CLOSE = "Close"

class Role(Enum):
    ENGINEER = "Engineer"
    ADMIN = "Admin"
    CUSTOMER = "Customer"

class Location(Enum):
    BANGALORE = "Bangalore"
    CHENNAI = "Chennai"
    PUNE = "Pune"
    HYDERABAD = "Hyderabad"

class CreateUser(BaseModel):
    name: str
    role: Role

class OutageCreate(BaseModel):
    name: str
    location: Location
    status: Status
    engineer_id: str