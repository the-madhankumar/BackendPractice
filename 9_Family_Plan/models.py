from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Family(Base):
    __tablename__ = "family_management_families"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    users = relationship("User", back_populates="family")


class User(Base):
    __tablename__ = "family_management_users"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("family_management_families.id"))
    name = Column(String(100))
    is_primary = Column(Boolean, default=False)

    family = relationship("Family", back_populates="users")