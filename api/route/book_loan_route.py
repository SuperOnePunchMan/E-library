from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..service.book_loan_service import BookLoanService
from ..schemas.book_schema import AddBookRequest
from ..dependencies import role_required, get_current_user
from ..utils import success_response
from ..db import get_db


loan_book = APIRouter(prefix="/loan", tags=["loan"])

@loan_book.post(path="/loan_route/{book_id}",
            status_code= 200,
            response_model= success_response,
            summary= "Loan service",
            responses=
            {
                200:{
                    "description": " Borrow Book",
                    "content": {
                        "Application/json":{
                            "example":{
                                "Message": "Borrowed book successfully",
                                "Status":200,
                                "data":{}
                            }
                        }
                    }
                },
                400:{
                    "description": "Bad Request",
                    "content":{
                        "Application/json":{
                            "example":{
                                "Message": "Bad Request",
                                "Status":400,
                                "data":{}
                                }
                            }
                        }
                    },
                401:{
                    "description": "Unauthorized",
                    "content":{
                        "Application/json":{
                            "example":{
                                "Message": "UNAUTHORIZED",
                                "Status":401,
                                "data": {}
                            }
                        }
                    }
                }
            }
            )

def loan_book_route(book_id:int,db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    user_id= current_user.get("id")
    borrow= BookLoanService.loan_book(db=db, book_id=book_id, user_id=user_id)
    return borrow