from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from models import User

def require_primary(
    current_user_id: int,
    db: Session = Depends(get_db)
):
    current_user = db.get(User, current_user_id)

    if current_user is None:
        return {
            "error": "User Not Found"
        }
    if current_user.is_primary == False:
        return {
            "error": "Invalid Primary User"
        }

    return current_user