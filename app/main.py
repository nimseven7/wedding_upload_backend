from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.getenv("UPLOAD_DIR")

@app.post("/uploads/")
async def upload_file(files: list[UploadFile]):
    for file in files:
        with open(f"uploads/{file.filename}", "wb") as buffer:
            buffer.write(await file.read())
    return {"status": "Upload success!"}