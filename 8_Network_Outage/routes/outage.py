from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import CreateUser, OutageCreate, Role
from models import User, Outage
from database import get_db

router = APIRouter()


@router.post("/create-user")
def create_user(data: CreateUser, db: Session = Depends(get_db)):

    new_user = User(
        name=data.name,
        role=data.role.value
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "New User Created Successfully",
        "user": new_user
    }


@router.post("/outage/{user_id}")
def create_outage(user_id: int, data: OutageCreate, db: Session = Depends(get_db)):

    current_user = db.get(User, user_id)

    if current_user is None:
        return {"Error": "User Not Found"}

    if current_user.role != Role.ADMIN.value:
        return {"Error": "Only Admin Can Create Outage"}

    new_outage = Outage(
        name=data.name,
        status=data.status.value,
        location=data.location.value,
        engineer_id=data.engineer_id
    )

    db.add(new_outage)
    db.commit()
    db.refresh(new_outage)

    return {
        "message": "Outage Created Successfully",
        "outage": new_outage
    }


@router.put("/outage/{user_id}/{outage_id}")
def update_outage(
    user_id: int,
    outage_id: int,
    data: OutageCreate,
    db: Session = Depends(get_db)
):

    current_user = db.get(User, user_id)

    if current_user is None:
        return {"Error": "User Not Found"}

    if current_user.role != Role.ENGINEER.value:
        return {"Error": "Only Engineer Can Update Outage"}

    outage = db.get(Outage, outage_id)

    if outage is None:
        return {"Error": "Outage Not Found"}

    if outage.engineer_id != user_id:
        return {"Error": "Engineer Not Assigned To This Outage"}

    outage.name = data.name
    outage.status = data.status.value
    outage.location = data.location.value
    outage.engineer_id = data.engineer_id

    db.commit()
    db.refresh(outage)

    return {
        "message": "Outage Updated Successfully",
        "outage": outage
    }


@router.delete("/outage/{user_id}/{outage_id}")
def delete_outage(
    user_id: int,
    outage_id: int,
    db: Session = Depends(get_db)
):

    current_user = db.get(User, user_id)

    if current_user is None:
        return {"Error": "User Not Found"}

    if current_user.role != Role.ADMIN.value:
        return {"Error": "Only Admin Can Delete Outage"}

    outage = db.get(Outage, outage_id)

    if outage is None:
        return {"Error": "Outage Not Found"}

    db.delete(outage)
    db.commit()

    return {
        "message": "Outage Deleted Successfully"
    }


@router.get("/outage/{user_id}")
def get_outages(user_id: int, db: Session = Depends(get_db)):

    current_user = db.get(User, user_id)

    if current_user is None:
        return {"Error": "User Not Found"}

    if current_user.role != Role.CUSTOMER.value:
        return {"Error": "Only Customer Can View Outages"}

    outages = db.query(Outage).all()

    return {
        "message": "Outages Retrieved Successfully",
        "outages": outages
    }