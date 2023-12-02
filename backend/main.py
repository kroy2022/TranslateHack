from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PRIVATE_KEY='f06a64ca-b272-4589-96f5-1ed1fd0ea09b'

class User(BaseModel):
    username: str

@app.post('/authenticate')
async def authenticate(user: User):
    response = requests.put('https://api.chatengine.io/users/',
        data = {
            "username": user.username,
            "secret": user.username,
            "first_name": user.username,
        },
        headers={"Private-Key": PRIVATE_KEY}
    )
    return response.json()

@app.post("/translateMessage")
async def translate(message: dict):
    incoming_message = message.get("message", " ")
    translated_message = incoming_message + " Added "
    return {"translated_message": translated_message}
#projectID: 7c2c3ea1-3c0e-4a99-a456-bea13d6a618b


