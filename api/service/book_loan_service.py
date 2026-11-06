from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from ..models.book_model import BookLoan,Book
from ..schemas.book_schema import AddBookRequest
from ..utils import success_response



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
            book= db.query(Book).filter_by(id=book_id).first()
            if not book:
                raise HTTPException(status_code=400, detail= " Invalid Book_Id")
            if book.quantity == 0:
                raise HTTPException(status_code=400, detail="Book not Available! Check back at a different date")
            background_check(db=db, user_id=user_id)
            duplicate_check= db.query(BookLoan).filter_by(book_id=book_id, user_id=user_id, return_status=False).first()
            if duplicate_check:
                raise HTTPException(status_code=400,
                                    detail="You Have already borrowed a Book and Yet To Return")
            new_book_loan= BookLoan(
                book_id=book_id,
                user_id=user_id
            )
            print(book.quantity)
            book.quantity = book.quantity-1
            db.add(new_book_loan)
            db.commit()
            db.refresh(new_book_loan)
            return success_response(status_code= 200, message="You have successfully loaned a book")
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def return_book_service(db:Session, book_loan_id:int, user_id:int):
        try:
            book_loan_check= db.query(BookLoan).filter_by(id=book_loan_id).first()
            if book_loan_check:
                book_loan_check.return_status= True
                book_id= book_loan_check.book_id
                book_seen= db.query(Book).filter_by(id=book_id).first()
                book_seen.quantity += 1
                db.commit()
                return success_response(status_code=200, message="Book returned successfully")
            raise HTTPException(status_code= 400, detail=" Book Loan Id Not Found")
        except Exception as e:
            raise HTTPException(status_code= 500, detail= str(e))

    @staticmethod
    def user_loan_history(db:Session, user_id:int):
        try:
            loan_history= db.query(BookLoan).filter_by(user_id=user_id).all()
            if not loan_history:
                return {"status code":200, "Message": "You Have no Loan History"}
            result=[{"id": loan.id,
                     "book_id": loan.book_id,
                     "date_borrowed": loan.date_borrowed.isoformat() if loan.date_borrowed else None,
                     "expected_return_date":loan.expected_return_date.isoformat() if loan.expected_return_date else None,
                     "return_status": loan.return_status}for loan in loan_history]
            return success_response(status_code=200, message="Book Loan History retrieved Successfully", data=result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
