from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Customer, Bill, Payment
from schemas import GenerateBillRequest, BillResponse, PaymentResponse, PayBillRequest
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

@router.post("/pay-bill", response_model=PaymentResponse)
def pay_bill(data: PayBillRequest, db: Session = Depends(get_db)):
    bill = db.get(Bill, data.bill_id)
    if bill is None:
        raise HTTPException(status_code=404, detail="Bill Not Found")
    
    new_payment = Payment(
        bill_id=data.bill_id,
        amount=data.amount,
        transaction_id=data.transaction_id
    )

    db.add(new_payment)

    db.commit()
    db.refresh(new_payment)

    return {
        "Status": "Payment Successfull",
        "data": new_payment
    }

@router.get("/bill/{bill_id}")
def get_bill(bill_id: int, db: Session = Depends(get_db)):
    bill = db.get(Bill, bill_id)

    if bill is None:
        return HTTPException(status_code=404, detail="No bill Found")

    return bill

@router.get("/bill/history/{customer_id}")
def get_customer_bills(customer_id: int, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    bills = (
        db.query(Bill)
        .filter(Bill.customer_id == customer_id)
        .all()
    )

    return bills