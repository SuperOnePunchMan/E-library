
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base

class Permission(Base):
    __tablename__ = "permissions"
    id= Column(Integer,primary_key=True)
    name = Column(String, unique = True, nullable = False)
    role_permission= relationship("RolePermission", back_populates="permission")


class RolePermission(Base):
    __tablename__ = "role_permissions"
    id= Column(Integer, primary_key= True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    permission_id = Column(Integer, ForeignKey("permissions.id"))
    role= relationship("Role", back_populates= "role_permission")
    permission = relationship("Permission", back_populates="role_permission")
    
