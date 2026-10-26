from ..dependencies import role_required, get_current_user
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from ..models.user_model import User
from ..models.book_model import Book, BookLoan
from ..schemas.book_schema import AddBookRequest, UpdateBookRequest
from ..utils import success_response, failure_response


class LibraryService:
    @staticmethod
    def add_book(db:Session, book_data:AddBookRequest)->dict:
        try:
            book_check = db.query(Book).filter_by(isbn=book_data.isbn).first()
            if book_check:
                return failure_response(message= " Book with this information already exsists",
                        status_code=400)
            new_book= Book(
                title =book_data.title,
                genre= book_data.genre,
                author = book_data.author,
                publisher = book_data.publisher,
                year_of_publication = book_data.year_of_publication,
                number_of_pages = book_data.number_of_pages,
                quantity= book_data.quantity,
                language= book_data.language,
                isbn= book_data.isbn

            )
            db.add(new_book)
            db.commit()
            return success_response(status_code=200, message="Book added successfully")

        except Exception as e:
            raise HTTPException(status_code= 400, detail=str(e))


    @staticmethod
    def get_all_books(db:Session):
        books=db.query(Book).all()
        item= [{ "id": book.id,
                "title": book.title,
                "genre":book.genre,
                "author": book.author,
                "publisher":book.publisher,
                "year_of_publication":book.year_of_publication,
                "number_of_pages":book.number_of_pages,
                "language":book.language,
                "isbn":book.isbn}for book in books ]
        return success_response(status_code=200, message="Books Retrived With Success", data= item)

    @staticmethod
    def get_book_by_id(db:Session, id:int):
        try:
            retrieve_book= db.query(Book).filter_by(id= id).first()
            if not retrieve_book:
                return failure_response(status_code= 404, message=" Book not found")
            book= AddBookRequest.model_validate(retrieve_book).model_dump()
            return success_response(status_code=200, message= "Book found!", data= book)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e) )

    @staticmethod
    def update_book_by_id(db:Session, id:int, update_request:UpdateBookRequest):
        try:
            retrieve_book= db.query(Book).filter_by(id= id).first()
            if not retrieve_book:
                return failure_response(status_code= 404, message=" Book not found")
            
            book= update_request.model_dump(exclude_unset= True)
            for field, value in book.items():
                setattr(retrieve_book, field, value)

            db.commit()
            db.refresh(retrieve_book)
            updated_book= {"id": retrieve_book.id,
                           "title": retrieve_book.title,
                           "genre":retrieve_book.genre,
                           "author": retrieve_book.author,
                           "publisher":retrieve_book.publisher,
                           "year_of_publication":retrieve_book.publisher,
                           "number_of_pages":retrieve_book.number_of_pages,
                           "language":retrieve_book.language,
                           "isbn": retrieve_book.isbn}
            return success_response(status_code=200, message= "Book found!", data= book)
        except Exception as e:
            raise HTTPException(status_code=400, detail= str(e))
        
    @staticmethod
    def delete_book_by_id(db:Session, id:int):
        try:
            retrieve_book= db.query(Book).filter_by(id=id).first()
            if not retrieve_book:
                return failure_response(status_code=404, message="Book not found!")
            db.delete(retrieve_book)
            db.commit()
            return success_response(status_code=200, message= "Book deleted succesfully")
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail= str(e))
