from sqlalchemy.orm import Session
from api.models.roles import RoleEnum, Role
from api.db import SessionLocal
from api.models.permission import RolePermission, Permission

DEFAULT_PERMISSION= {
    RoleEnum.USER: [
        "borrow_books", 
        "view_books",
        "return_books"
    ],
    RoleEnum.LIBRARIAN:[
        "edit_books",
        "add_books",
        "delete_books",
        "view_user",
        "loan_out_book"
    ]
} 

def seed_roles_permissions(db:Session):
    for x in RoleEnum:
        role= db.query(Role).filter_by(name=x).first()
        if not role:
            new_role=Role(name=x)
            db.add(new_role)
    db.commit()

    all_permission_names = set(p for permission in DEFAULT_PERMISSION.values() for p in permission)
    for perm_name in all_permission_names:
        perm= db.query(Permission).filter_by(name= perm_name).first()
        if not perm:
            new_perm= Permission(name=perm_name)
            db.add(new_perm)
    db.commit()

    for role_enum, perm_names in DEFAULT_PERMISSION.items():
        role = db.query(Role).filter_by(name= role_enum).first()
        for perm_name in perm_names:
            permission = db.query(Permission).filter_by(name=perm_name).first()
            exsists = db.query(RolePermission).filter_by(role_id= role.id, permission_id= permission.id).first()
            if not exsists:
                new_role_permission = RolePermission(role_id= role.id, permission_id= permission.id)
                db.add(new_role_permission)
    db.commit()
    print("role and permission seeded successfully")


if __name__ == "__main__":
    db= SessionLocal()
    try:
        seed_roles_permissions(db)
    finally:
        db.close()