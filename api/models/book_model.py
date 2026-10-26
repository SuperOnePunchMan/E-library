from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from ..db import Base
from .user_model import User
from datetime import datetime, timedelta

class Book(Base):
    __tablename__ = "books"
    id= Column(Integer, primary_key=True)
    title= Column(String, nullable=False)
    genre= Column(String, nullable=False)
    author= Column(String, nullable=False)
    publisher= Column(String, nullable=False)
    year_of_publication= Column(String,nullable=False)
    number_of_pages= Column(String, nullable=False)
    quantity= Column(Integer, default=1)
    language= Column(String, nullable=False)
    isbn= Column(String, nullable=False, unique=True)
    book_loan= relationship("BookLoan", back_populates="book")



class BookLoan(Base):
    __tablename__ = "bookloans"
    id= Column(Integer, primary_key= True)
    book_id= Column(Integer,ForeignKey("books.id"))
    user_id= Column(Integer, ForeignKey("users.id"))
    date_borrowed= Column(String, default=datetime.now())
    expected_return_date=Column(DateTime, nullable=True)
    return_status= Column(Boolean, default=False)
    book = relationship("Book", back_populates="book_loan" )
    user= relationship("User", back_populates= "loan")

    def __init__(self,book_id,user_id, return_date=None):
        #super().__init__()
        self.book_id= book_id
        self.user_id= user_id
        self.expected_return_date= return_date

    def caculate_expected_return_date(self):
        if self.date_borrowed:
            self.expected_return_date= self.date_borrowed + timedelta(days=7)



