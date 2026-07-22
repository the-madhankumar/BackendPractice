from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from routes.middleware import require_primary
from models import Family, User
from schemas import CreateFamily, AddMember

router = APIRouter(prefix="/family")


@router.post("/")
def create_family(
    data: CreateFamily,
    db: Session = Depends(get_db)
):
    new_family = Family(
        name=data.family_name
    )

    db.add(new_family)
    db.flush()

    new_user = User(
        family_id=new_family.id,
        name=data.primary_name,
        is_primary=True
    )

    db.add(new_user)
    db.commit()

    return {
        "family_id": new_family.id,
        "message": "Family created successfully"
    }


@router.post("/add-member")
def add_member(
    data: AddMember,
    current_user: User = Depends(require_primary),
    db: Session = Depends(get_db)
):
    new_member = User(
        family_id=current_user.family_id,
        name=data.name,
        is_primary=False
    )

    db.add(new_member)
    db.commit()

    return {
        "message": "Member added successfully"
    }


@router.delete("/member/{member_id}")
def delete_member(
    member_id: int,
    current_user: User = Depends(require_primary),
    db: Session = Depends(get_db)
):
    if isinstance(current_user, dict):
        return current_user
    
    member = (
        db.query(User)
        .filter(
            User.id == member_id,
            User.family_id == current_user.family_id
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    if member.is_primary:
        raise HTTPException(
            status_code=400,
            detail="Primary member cannot be deleted"
        )

    db.delete(member)
    db.commit()

    return {
        "message": "Member deleted successfully"
    }


@router.get("/{family_id}")
def get_family(
    family_id: int,
    db: Session = Depends(get_db)
):
    family = (
        db.query(Family)
        .filter(Family.id == family_id)
        .first()
    )

    if family is None:
        raise HTTPException(
            status_code=404,
            detail="Family not found"
        )

    return {
        "id": family.id,
        "name": family.name,
        "users": family.users
    }