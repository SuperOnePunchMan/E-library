from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.orm import Session
from ..db import get_db
from ..schemas.auth_schema import SignupRequest, verification_request, LoginRequest, forget_password_request, change_password_request 
from ..service.auth_service import AuthService

auth_route= APIRouter(prefix="/auth",tags=["authentication"])

@auth_route.post(path="/signup",
           status_code= status.HTTP_201_CREATED,
           summary= " Signing up a new or exsisting user",
           responses={
               201:{
                        "description": "User Signed up successfully! to continue verify your email address.",
                        "content": {
                            "Application/json":{
                                "example":{
                                "Message": " PLease Verify Your account with the Otp sent to the email provided above",
                                    "Status":201,
                                    "data":{}
                                }
                            }
                        }
                    },
                400:{
                        "description":" Bad Request, invalid input or data validation error",
                        "content":{
                                    "Application/json":{
                                        "example":{
                                        "Message": " Bad Request",
                                        "Status":400,
                                        "data":{}
                                        }
                                    }
                        }
                    },
                409:{
                        "description": "Conflict, email already exsists",
                        "content": {
                        "Application/json":{
                                "example":{
                                "Message": " Conflict",
                                    "Status": 409,
                                    "data":{}
                                }
                            }
                        }
                }
           })
async def register(user_data:SignupRequest, db:Session=Depends(get_db)):
    registered_user= await AuthService.signup(db=db, user_data=user_data)
    return registered_user



@auth_route.post(path="/verify",
           status_code=201,
            summary= "Verify an Otp",
           responses={
                201:{
                        "description": " User Succesfully Verified their Otp ",
                        "content": {
                            "Application/json": {
                                "example": {
                                "Message": "OTP SUCCESFULLY VERIFIED!!",
                                    "Status":201, 
                                    "data":{}  
                                }
                            }
                        }
                    },
                400:{
                        "description": "Bad Request, invalid input or data validation error",
                        "content":{
                                    "Application/json": {
                                        "example": {
                                        "Message": "Invalid OR Expired Otp Provided",
                                        "Status":400, 
                                        "data":{}  
                                        } 
                                    }
                                }
                    }
                }
        )
def otp_verification(user_data:verification_request, db:Session=Depends(get_db))->dict:
    new_user = AuthService.verify_otp(db= db, user_data= user_data)
    return new_user


@auth_route.post (path="/login",
            status_code=200,
            summary= "Login",
            responses={
                200:{
                        "description": " User Succesfully Logged in ",
                        "content": {
                            "Application/json": {
                                "example": {
                                "Message": "Uaer Successfully Logged in",
                                    "Status":200, 
                                    "data":{}  
                                }
                            }
                        }
                    },
                400:{
                        "description": "Bad Request, Invalid Login",
                        "content":{
                                    "Application/json": {
                                        "example": {
                                        "Message": "Invalid  Email or Password Provided",
                                        "Status":400, 
                                        "data":{}  
                                        } 
                                    }
                                }
                    }
                }
            )


def login_route(user_data: LoginRequest, db:Session=Depends(get_db)):
    user = AuthService.login(db=db, user_data= user_data)
    return user



@auth_route.post(path="/forget_password",
            status_code=200,
            summary= "Forget",
            responses={
                200:{
                        "description": " initiate password change",
                        "content": {
                            "Application/json": {
                                "example": {
                                "Message": "Password reset initiated succesfully",
                                    "Status":200, 
                                    "data":{}  
                                }
                            }
                        }
                    },
                400:{
                        "description": "Bad Request",
                        "content":{
                                    "Application/json": {
                                        "example": {
                                        "Message": "Invalid email",
                                        "Status":400, 
                                        "data":{}  
                                        } 
                                    }
                                }
                    }
                }
            )


async def forget_password_route(user_data:forget_password_request, db:Session=Depends(get_db))->dict:
    user= await AuthService.forget_password_service(db=db, user_data=user_data)
    return user


@auth_route.patch(path="/reset_password",
            status_code=200,
            summary= "Change",
            responses={
                200:{
                        "description": "change pasword",
                        "content": {
                            "Application/json": {
                                "example": {
                                "Message": "Password reset succesfully",
                                    "Status":200, 
                                    "data":{}  
                                }
                            }
                        }
                    },
                400:{
                        "description": "Bad Request",
                        "content":{
                                    "Application/json": {
                                        "example": {
                                        "Message": "Invalid email",
                                        "Status":400, 
                                        "data":{}  
                                        } 
                                    }
                                }
                    }
                }
            )


async def reset_password_route(user_data:change_password_request, db:Session=Depends(get_db)):
    user=  await AuthService.reset_password_service(db=db, user_data= user_data)
    return user
