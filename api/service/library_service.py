from ..dependencies import role_required, get_current_user
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from ..models.user_model import User
from ..models.book_model import Book, BookLoan
from ..schemas.book_schema import AddBookRequest


class LibraryService:
    @staticmethod
    def add_book(db:Session, book_data:AddBookRequest)->dict:
        try:
            book_check = db.query(Book).filter_by(isbn=book_data.isbn).first()
            if book_check:
                return {"message": " Book with this information already exsists",
                        "status":status.HTTP_400_BAD_REQUEST}
            new_book= Book(
                title =book_data.title,
                genre= book_data.genre,
                author = book_data.author,
                publisher = book_data.publisher,
                year_of_publication = book_data.year_of_publication,
                number_of_pages = book_data.number_of_pages,
                language= book_data.language
            )
            db.add(new_book)
            db.commit()
            return {
                "message":"Book added successfully",
                "status": 201,
                "data": new_book
            }

        except Exception as e:
            raise HTTPException(status_code= 400, detail=str(e))