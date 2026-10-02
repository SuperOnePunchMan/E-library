from pydantic import BaseModel, Field, model_validator, field_validator

class AddBookRequest(BaseModel):
    title:str = Field()
    genre:str = Field()
    author:str= Field()
    publisher:str= Field()
    year_of_publication:str= Field()
    number_of_pages:str= Field()
    language: str= Field()
    isbn: str=Field()

    class Config:
        from_attributes= True
