from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def out():
    return "Hello World"

@app.get("/items/{id}")
def out1(id:str):
    return id.capitalize()
    