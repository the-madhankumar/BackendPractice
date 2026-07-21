from sqlalchemy import Column, Integer, String, BigInteger
from database import Base

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    number = Column(BigInteger)
    points = Column(Integer, default=0)