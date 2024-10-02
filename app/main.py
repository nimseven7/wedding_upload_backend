from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import imghdr

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
async def upload_file(files: list[UploadFile], foldername: str = Form('anonymous')):
    folder_path = os.path.join(UPLOAD_DIR, foldername)
    os.makedirs(folder_path, exist_ok=True)
    
    for file in files:
        # Check if the file is an image
        file_content = await file.read()
        if imghdr.what(None, h=file_content) is None:
            raise HTTPException(status_code=400, detail="Only image files are allowed")
        
        file_path = os.path.join(folder_path, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
    
    return {"status": "Upload success!"}