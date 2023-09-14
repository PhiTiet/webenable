from fastapi import FastAPI
from pydantic import BaseModel

class MyResponse(BaseModel):
    message: str = "Hello World"

app = FastAPI()


@app.get("/")
async def root() -> MyResponse:
    return MyResponse()
