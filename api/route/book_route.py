from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.orm import Session
from ..db import get_db
from ..schemas.book_schema import AddBookRequest
from ..service.library_service import LibraryService
from ..dependencies import role_required
from ..utils import success_response, failure_response

book_route= APIRouter(prefix="/book",tags=["library"])



@book_route.post(path="/library_route",
            status_code= 200,
            response_model= success_response,
            summary= "Library service",
            responses=
            {
                200:{
                    "description": " Add Book Information",
                    "content": {
                        "Application/json":{
                            "example":{
                                "Message": "Added book successfully",
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

def add_book_route (book_data:AddBookRequest, db:Session= Depends(get_db), current_user=Depends(role_required(["librarian"])))->dict[str,any]:
    new_book= LibraryService.add_book(db=db,book_data=book_data)
    return success_response(status_code=200, message="Book added successfully", data= new_book)