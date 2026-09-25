from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base
from .user_model import User
from datetime import datetime

class Book(Base):
    __tablename__ = "books"
    id= Column(Integer, primary_key=True)
    title= Column(String, nullable=False)
    genre= Column(String, nullable=False)
    author= Column(String, nullable=False)
    publisher= Column(String, nullable=False)
    year_of_publication= Column(String,nullable=False)
    number_of_pages= Column(String, nullable=False)
    language= Column(String, nullable=False)
    isbn= Column(String, nullable=False, unique=True)
    book_loan= relationship("BookLoan", back_populates="book")



class BookLoan(Base):
    __tablename__ = "bookloans"
    id= Column(String, primary_key= True)
    book_id= Column(Integer,ForeignKey("books.id"))
    user_id= Column(Integer, ForeignKey("users.id"))
    date_borrowed= Column(String, default=datetime.now())
    book = relationship("Book", back_populates="book_loan" )
    user= relationship("User", back_populates= "loan")




