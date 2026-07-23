from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Numeric, Date, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(BigInteger, unique=True, nullable=False)
    status = Column(String(20), nullable=False, default="ACTIVE")

    bills = relationship("Bill", back_populates="customer")

class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)
    penalty = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(10, 2), nullable=False)

    bill_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)

    status = Column(String(20), default="GENERATED")
    paid_at = Column(DateTime, nullable=True)

    customer = relationship("Customer", back_populates="bills")
    payments = relationship("Payment", back_populates="bills") 

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)
    transaction_id = Column(String(100), unique=True)
    payment_date = Column(DateTime)

    bill = relationship("Bill", back_populates="payments")