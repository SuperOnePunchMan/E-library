from fastapi import Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from .models.user_model import User
import jwt,os
from decouple import config
from .db import get_db
from dotenv import load_dotenv

load_dotenv()


def get_current_user(request:Request,db:Session=Depends(get_db))->User:
    try:
        token= request.cookies.get("access_token")
        if token is None:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail=" Invalid token")
    
        payload= jwt.decode(token, os.getenv("JWT_SECRET_KEY"),
                            algorithms=os.getenv("ALGORITHM"))
        print(payload)
        user_id= payload.get("id")
        role= payload.get("role")
        if user_id is None:
            raise HTTPException(status_code=401,
                                detail="Invalid or expired token")
        return{"id":user_id, "role": role}

    except Exception as e:
        raise HTTPException(status_code=401,
                            detail=str(e))


def role_required(allowed_roles:list):
    """Dependency to state which role allow to access particular route"""
    def role_checker(current_user:User=Depends(get_current_user)):
        if current_user.get("role") not in allowed_roles:
            raise HTTPException (status_code= status.HTTP_403_FORBIDDEN,
                                 detail= " You do not have permission to access this resource")
        return current_user
    return role_checker