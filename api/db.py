from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from decouple import config


SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind= create_engine(config("DB_URL")))
db_session = scoped_session(SessionLocal)

Base= declarative_base()

def get_db():
    db= db_session()
    try:
        yield db
    finally:
        db.close()