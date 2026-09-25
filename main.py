from fastapi import FastAPI, APIRouter
from api.route import api_version_one

app = FastAPI()

app.include_router(api_version_one)

@app.get("/")
def home():
    return {"Mesage": " Hello world"}


#if __name__ == "__main__":
#    app.run()
