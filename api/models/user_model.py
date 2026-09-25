
from sqlalchemy import Column, String, Boolean, ForeignKey, Enum, Integer
from sqlalchemy.orm import relationship
from enum import Enum as pyEnum
from ..db import Base

class GenderEnum(str,pyEnum):
    MALE= "male"
    FEMALE="female"


class User(Base):
    __tablename__ = "users"
    id= Column(Integer, primary_key= True)
    first_name = Column(String, nullable= False)
    last_name = Column(String, nullable= False)
    email = Column(String, unique= True, nullable= False)
    password= Column(String, nullable= False)
    phone = Column(String, unique=True, nullable= False)
    address = Column(String, nullable=False)
    gender = Column(Enum(GenderEnum),nullable= False)
    role_id= Column(String, ForeignKey("roles.id"), nullable= False, default =1)
    role = relationship("Role", back_populates= "user")
    loan= relationship("BookLoan", back_populates= "user")


