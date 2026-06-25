from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
from datetime import datetime

def create_user(db:Session,user_data:UserCreate,password_hash:str):
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
        created_at= datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_email(db:Session,email:str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db:Session, user_id:int):
    return db.query(User).filter(User.id == user_id).first()

