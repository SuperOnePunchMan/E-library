
from sqlalchemy import Column, String, Integer, Enum as sqlEnum
from sqlalchemy.orm import relationship
from enum import Enum as pyEnum
from ..db import Base

class RoleEnum(str, pyEnum):
    USER= "user"
    LIBRARIAN = "librarian"
    ADMIN = "admin" 
    

class Role(Base):
    __tablename__ = "roles"
    id= Column(Integer, primary_key=True)
    name= Column(sqlEnum(RoleEnum), nullable= False)
    role_permission=relationship("RolePermission", back_populates= "role")
    user = relationship("User", back_populates= "role")
