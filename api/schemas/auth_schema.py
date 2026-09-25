from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator
from ..models.user_model import GenderEnum

def NormaliseValue(v):
    return v.lower() if isinstance(v, str) else v



class CleanBaseModel(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def clean(cls,values):
        return{
            k: v.strip() if isinstance(v,str) else v
            for k, v in values.items() 
        }




class SignupRequest(CleanBaseModel):
    first_name:str = Field()
    last_name:str = Field()
    email:EmailStr = Field()
    password: str = Field()
    confirm_password: str = Field()
    phone:str = Field(...,min_lenght=9, max_lenght= 11)
    address:str = Field()
    gender:GenderEnum = Field()


    @field_validator("phone", mode="before")
    @classmethod
    def normalised_phone(cls, v):
        if v and not v.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            raise ValueError ("Phone number must contain only digits, spaces, hyphens, plus signs!")
        return v

    @field_validator("gender", mode="before")
    @classmethod
    def gender(cls, v):
        return NormaliseValue(v)

    @field_validator("confirm_password")
    @classmethod
    def password_match(cls, v, values):
        if values.data.get("password") and v != values.data["password"]:
            raise ValueError("Passwords do not match")
        return v

    class Config:
        use_enum_values = True


class LoginRequest(BaseModel):
    email:EmailStr = Field()
    password: str = Field()

class verification_request(BaseModel):
    email:EmailStr = Field()
    otp:int = Field()

class forget_password_request(BaseModel):
    email:EmailStr= Field()

class change_password_request(BaseModel):
    email:EmailStr = Field()
    otp:int= Field()
    new_password: str = Field()
    confirm_password: str= Field()
