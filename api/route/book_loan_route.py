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


@loan_book.post(path="/return_book_route/{book_loan_id}",
            status_code= 200,
            response_model= success_response,
            summary= "Return Book Loan",
            responses=
            {
                200:{
                    "description": " Return Book",
                    "content": {
                        "Application/json":{
                            "example":{
                                "Message": " Returned book successfully",
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

def return_book_route(book_loan_id:int, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    user_id=current_user.get("id")
    book_return= BookLoanService.return_book_service(db=db, book_loan_id=book_loan_id, user_id=user_id)
    return book_return

@loan_book.post(path="/user_loan_history",
            status_code= 200,
            response_model= success_response,
            summary= "Book Loan History",
            responses=
            {
                200:{
                    "description": " User History",
                    "content": {
                        "Application/json":{
                            "example":{
                                "Message": " Book Loan History retrieved Successfully ",
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

def user_loan_history(db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    user_id= current_user.get("id")
    loan_history= BookLoanService.user_loan_history(db=db, user_id=user_id)
    return loan_history