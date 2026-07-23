from sqlalchemy import Column, Integer, String, ForeignKey

from database import Base

class User(Base):
    __tablename__ = "Network_Outage_Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    role = Column(String(20))

class Outage(Base):
    __tablename__ = "Network_Outage_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    location = Column(String(20))
    status = Column(String(20))

    engineer_id = Column(Integer, ForeignKey("Network_Outage_Users.id"))