from pydantic import BaseModel, Field, model_validator, field_validator, ConfigDict

class AddBookRequest(BaseModel):
    title:str = Field()
    genre:str = Field()
    author:str= Field()
    publisher:str= Field()
    year_of_publication:str= Field()
    number_of_pages:str= Field()
    language: str= Field()
    isbn: str=Field()

    model_config=ConfigDict(from_attributes=True)


class UpdateBookRequest(BaseModel):
    title:str | None=None
    genre:str | None=None
    author:str | None=None
    publisher:str | None=None
    year_of_publication:str | None=None
    number_of_pages:str | None=None
    language: str | None=None