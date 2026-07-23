from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Customer, Bill
from schemas import GenerateBillRequest, BillResponse
from schemas import CustomerCreate, CustomerResponse

router = APIRouter()

@router.post("/create-customer")
def create_customer(data: CustomerCreate, db: Session = Depends(get_db), response_model=CustomerResponse):
    new_customer = Customer(
        name=data.name,
        email=data.email,
        phone=data.phone
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return {
        "message": "Customer Created Successfully",
        "data": new_customer
    }

@router.post("/generate-bill", response_model=BillResponse)
def generate_bill(data: GenerateBillRequest, db: Session = Depends(get_db)):

    customer = db.query(Customer).filter(Customer.id == data.customer_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    today = date.today()

    existing_bill = (
        db.query(Bill)
        .filter(
            Bill.customer_id == data.customer_id,
        )
        .first()
    )

    bill = Bill(
        customer_id=data.customer_id,
        amount=data.amount,
        penalty=0,
        total_amount=data.amount,
        bill_date=today,
        due_date=today + timedelta(days=15),
        status="GENERATED",
    )

    db.add(bill)
    db.commit()
    db.refresh(bill)

    return bill