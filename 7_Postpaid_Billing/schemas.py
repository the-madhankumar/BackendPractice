from pydantic import BaseModel, EmailStr
from decimal import Decimal
from datetime import date, datetime

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: int

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: int
    status: str

class GenerateBillRequest(BaseModel):
    customer_id: int
    amount: Decimal

class BillResponse(BaseModel):
    id: int
    customer_id: int
    amount: Decimal
    penalty: Decimal
    total_amount: Decimal
    bill_date: date
    due_date: date
    status: str
    paid_at: datetime | None = None

class PayBillRequest(BaseModel):
    bill_id: int
    amount: Decimal
    transaction_id: str

class PaymentResponse(BaseModel):
    id: int
    bill_id: int
    amount: Decimal
    transaction_id: str