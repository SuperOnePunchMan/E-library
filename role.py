from sqlalchemy.orm import Session
from api.models.user_model import User
from api.models.roles import Role, RoleEnum
from api.db import SessionLocal

def role_udpdate(db:Session, email:str, target_role:str):
    email=email
    user_check= db.query(User).filter_by(email=email).first()
    if not user_check:
        print("No user found")
        return
    role_check=db.query(Role).filter_by(name=target_role).first()
    if not role_check:
        print("Role dosen't exsist")
        return

    user_check.role_id=role_check.id
    db.commit()
    print("Success, role updated successfully")
    return user_check

if __name__ == "__main__":
    db=SessionLocal()
    try:
        role_udpdate(db,email="jomi4lyfe@gmail.com", target_role="LIBRARIAN")
    finally:
        db.close() 
