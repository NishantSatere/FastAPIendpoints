from fastapi import FastAPI
from Routes.note import note

app = FastAPI()

app.include_router(note)