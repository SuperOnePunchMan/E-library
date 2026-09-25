import jwt, os, bcrypt, secrets, random
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException, status, Response, Request, Depends
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from ..models.user_model import User
from ..schemas.auth_schema import SignupRequest, verification_request, forget_password_request, change_password_request, LoginRequest
from ..utils import temp_db, success_response, failure_response
from ..mail import send_mail
from ..models.roles import Role

load_dotenv()

class AuthService:
    """"Service class for authentication operation"""

    @staticmethod
    def Hashpassword(password:str)->str:
        """This is to hash the user's password"""
        salt= bcrypt.gensalt()
        hash = bcrypt.hashpw((password).encode("utf-8"),salt)
        return hash.decode("utf-8")

    @staticmethod
    def Verifypassword(plain_password:str, hashed_password)->bool:
        """This is to verify the user's password"""
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    @staticmethod
    def create_access_token(data:dict, expiration_time:Optional[timedelta]=None):
        data_to_encode= data.copy()
        if expiration_time:
            expire= datetime.now(timezone.utc) + expiration_time
        else:
            expire=datetime.now(timezone.utc) + timedelta(minutes= int(os.getenv("ACCESS_TOKEN_EXPIRES")))
        data_to_encode.update({"exp":expire, "type": "access"})
        encode_jwt = jwt.encode(data_to_encode, secrets.token_hex(16))
        return encode_jwt

    @staticmethod
    def create_refresh_token(data:dict, expiration_time:Optional[timedelta]=None):
        data_to_encode= data.copy()
        if expiration_time:
            expire= datetime.now(timezone.utc) + expiration_time
        else:
            expire=datetime.now(timezone.utc) + timedelta(days= int(os.getenv("REFRESH_TOKEN_EXPIRES")))
        data_to_encode.update({"exp":expire, "type": "refresh"})
        encode_jwt = jwt.encode(data_to_encode, secrets.token_hex(16))
        return encode_jwt



    @staticmethod
    def otp_generator():
        return random.randint(1000, 9999)


    @staticmethod
    async def signup(db:Session, user_data:SignupRequest)->dict:
        try:
            first_name= user_data.first_name
            last_name= user_data.last_name
            email= user_data.email
            password= user_data.password
            phone= user_data.phone
            address= user_data.address
            gender= user_data.gender
            role = db.query(Role).filter_by(name="USER").first()
            print(role)
            if db.query(User).filter_by(email=email).first():
                raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= "email already exsists, Try Again")
            if db.query(User).filter_by(phone=phone).first():
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= "phone number already exsists")

            hash_password= AuthService.Hashpassword(password)
            otp= AuthService.otp_generator()
            b=temp_db()
            user_info = b.hset(email, mapping = {"first_name": first_name, 
                                                "last_name":last_name,
                                                "email": email, 
                                                "password": hash_password, 
                                                "otp":otp,
                                                "phone": phone,
                                                "address": address,
                                                "gender": gender,
                                                "role_id": role.id})
            temp_db().expire(email, 300)
            await send_mail(Subject = "otp verification", Recipients= [email], Template_name= "otp.html", Context= {"otp":otp})

            return{"Message": "Please Verify Your Account With the Otp Sent To The Email Provided Above",
                "Status":status.HTTP_201_CREATED} 
        except Exception as e:
            print (str(e))
            return{"Message": f"{str (e)}"}, status.HTTP_400_BAD_REQUEST

    @staticmethod
    def verify_otp(db:Session, user_data: verification_request)->dict:
        email= user_data.email
        otp= int(user_data.otp)
        user = temp_db().hgetall(email)
        if otp == int(user.get("otp")):
            new_user = User(first_name=user.get("first_name"),
                            last_name=user.get("last_name"), 
                            email=user.get("email"),
                            password= user.get("password"), 
                            phone=user.get("phone"), 
                            address= user.get("address"),
                            gender= user.get("gender"), 
                            role_id= user.get("role_id"))
            db.add(new_user)
            db.commit()
            temp_db().delete("email")
            return {"Message":"Successfull otp"}
        else:
            return{"Message": " Invalid OR Expired OtP, Please tRY again"}

    @staticmethod
    def login(db:Session, user_data:LoginRequest):
        try:
            email = user_data.email
            password= user_data.password
            user_access =db.query(User).filter_by(email=email).first()
            if not user_access:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="email or password incorrect")
            if not AuthService.Verifypassword(plain_password=password, hashed_password= user_access.password):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="email or passwprd incorrect")
            access_token= AuthService.create_access_token(data={"id": user_access.id, "email": user_access.email, "role": user_access.role_id})
            refresh_token= AuthService.create_refresh_token(data={"id": user_access.id, "email": user_access.email, "role": user_access.role_id})
            res =JSONResponse(
                status_code=200,
                content={
                    "message":"Login successfull",
                    "data":{
                        "access_token":access_token,
                        "refresh_token":refresh_token
                    }
                }
            )
            print(access_token)

            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                max_age= (int(os.getenv("ACCESS_TOKEN_EXPIRES"))*60),
                expires=(int(os.getenv("ACCESS_TOKEN_EXPIRES"))*60),
                secure=None,
                samesite="lax",
                path="/",
                domain=None
            )

            res.set_cookie(
                key= "refresh_token",
                value= refresh_token,
                httponly=True,
                max_age=(int(os.getenv("REFRESH_TOKEN_EXPIRES"))*3600),
                expires=(int(os.getenv("REFRESH_TOKEN_EXPIRES"))*3600),
                secure=None,
                samesite="lax",
                path="/",
                domain= None
            )

            return{"Message": "Successfull Login", "data": res}
        except Exception as e:
            raise HTTPException (status_code=400, detail=str(e))


    @staticmethod
    async def forget_password_service(db:Session, user_data:forget_password_request)->dict:
        try:
            email= user_data.email
            if db.query(User).filter(User.email== email).first():
                otp= AuthService.otp_generator()
                a=temp_db()
                user_info = a.hset(email, mapping= { "email": email, "otp":otp})
                temp_db().expire(email, 300)      
                await send_mail(Subject = "otp verification", Recipients= [email], Template_name= "otp.html", Context={"otp":otp})   
                return success_response(status_code= 200,
                                    message= "Please Verify Your Account With the Otp Sent To The Email",
                                    data= {})
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Invalid email provided ")
        except Exception as e:
            return{"Message": f"{str (e)}"}, status.HTTP_400_BAD_REQUEST


    @staticmethod
    async def reset_password_service(db:Session, user_data: change_password_request)->dict:
        email= user_data.email
        otp= int(user_data.otp)
        new_password= user_data.new_password
        confirm_password= user_data.confirm_password

        user = temp_db().hgetall(email)
        if otp == int(user.get("otp")):
            user = db.query(User).filter(User.email==email).first()
            hashpassword= AuthService.Hashpassword(new_password)
            user.password= hashpassword
            db.commit()
            return success_response(status_code= 200,
                                    message= " Password Reset Successfully",
                                    data= {})
        else:
            return{"Message": " Invalid OR Expired OtP, Please tRY again"}
