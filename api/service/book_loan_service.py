from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from ..models.book_model import BookLoan,Book
from ..schemas.book_schema import AddBookRequest



def background_check(user_id:int, db:Session):
    history_check= db.query(BookLoan).filter(BookLoan.user_id==user_id, BookLoan.return_status==False).count()
    if history_check > 5:
        raise HTTPException(status_code= 400, 
                            detail= "User has exceeded the maxium number of active book loan")
    overdue_check= db.query(BookLoan).filter(
        BookLoan.user_id == user_id,
        BookLoan.return_status == False,
        BookLoan.expected_return_date < datetime.now()
    ).first()
    if overdue_check:
        raise HTTPException(status_code=400,
                            detail=" User can't borrow new book because they have an overdue book" )
    return True



class BookLoanService:
    @staticmethod
    def loan_book(db:Session, book_id:int, user_id:int):
        try:
            book= db.query(Book).filter_by(id==book_id).first()
            if not book:
                raise HTTPException(status_code=400, detail= " Invalid Book_Id")
            if book.quantity == 0:
                raise HTTPException(status_code=400, details="Book not Available! Check back at a different date")
            background_check(db=db, user_id=user_id)
            print("background_check passed")
            new_book_loan= BookLoan(
                book_id=book_id,
                user_id=user_id
            )
            print(book.quantity)
            book.quantity = book.quantity-1
            db.add(new_book_loan)
            db.commit()
            db.refresh()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))