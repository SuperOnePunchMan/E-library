from fastapi import APIRouter
from .auth_route import auth_route
from .book_route import book_route
from .book_loan_route import loan_book

api_version_one= APIRouter(prefix="/api/v1")

api_version_one.include_router(auth_route)
api_version_one.include_router(book_route)
api_version_one.include_router(loan_book)