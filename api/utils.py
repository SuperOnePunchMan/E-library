import os
from typing import Optional, Dict
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException, status
import redis
from dotenv import load_dotenv

load_dotenv()

def temp_db():
    try:
        r = redis.Redis(
            host= os.getenv("REDIS_HOST"),
            port= os.getenv("REDIS_PORT"),
            decode_responses=True,
            username="default",
            password= os.getenv("REDIS_PASSWORD"),
        )
        return r
    except Exception as e:
        print("e")
        return(str(e))

    
def success_response(status_code:int, message: str, data: Optional[Dict]= None):
    response_data = {
        "status": "success",
        "message": message,
        "data": data or {}
    }
    return JSONResponse(status_code= status_code, content= response_data)

def failure_response(status_code:int, message: str, data: Optional[Dict]= None):
    response_data = {
        "status": "faliure",
        "message": message,
        "data": data or {}
    }
    return JSONResponse(status_code= status_code, content= response_data)
