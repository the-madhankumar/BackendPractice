from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserCreate, Recharge, Redeem

router = APIRouter()

global_id = 1
@router.post("/create-user")
def CreateUser(data: UserCreate, db: Session = Depends(get_db)):
    global global_id

    new_user = User(
        id = global_id,
        name = data.name,
        number = data.number
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    global_id += 1

    return {
        "Status": "Success",
        "message": "New User Created",
        "new_user": new_user
    }

@router.post("/reward/recharge/")
def do_recharge(data: Recharge, db: Session = Depends(get_db)):
    user_id = data.user_id
    current_user = db.get(User, user_id)

    if current_user is None:
        return {
            "error": "User Not Found"
        }
    
    if data.amount > 1000:
        current_user.points += 120
    elif data.amount > 500:
        current_user.points += 50
    
    db.commit()

    return {
        "status": "Success",
        "message": "Recharge Successfull"
    }

@router.get("/reward/points/{user_id}")
def get_points(user_id: int, db: Session = Depends(get_db)):
    current_user = db.get(User, user_id)

    if current_user is None:
        return {
            "error": "User Not Found"
        }

    return {
        "points": current_user.points
    }

@router.post("/reward/redeem")
def points(data: Redeem, db: Session = Depends(get_db)):
    user_id = data.user_id
    to_be_redeem_points = data.points

    current_user = db.get(User, user_id)
    if current_user.points >= to_be_redeem_points and to_be_redeem_points >= 200:
        current_user.points -= to_be_redeem_points
        db.commit()
        return {
            "status": "Success",
            "message": "Redemption Sucess"
        }
    else:
        return {
            "status": "Failed",
            "message": "Redemption Failed"
        }