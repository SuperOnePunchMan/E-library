from pydantic.v1 import BaseSettings
from decouple import config

class Settings(BaseSettings):
    PROJECT_NAME: str=config("APP_NAME")
    SECRET_KEY:str= config("SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRE: int= config("JWT_ACCESS_TOKEN_EXPIRE")
    JWT_REFRESH_TOKEN_EXPIRE: int= config("JWT_REFRESH_TOKEN_EXPIRE")
    JWT_ALGORITHM:str= config ("JWT_ALGORITHM")