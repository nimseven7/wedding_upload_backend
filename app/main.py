from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import imghdr
import mimetypes

load_dotenv()

STAGE = os.getenv("STAGE", "dev")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

app = FastAPI(docs_url=None, redoc_url=None) if STAGE == "prod" else FastAPI()

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
    
    allowed_video_types = ["video/mp4", "video/x-matroska", "video/x-msvideo", "video/x-ms-wmv"]

    for file in files:
        # Check if the file is an image or video
        file_content = await file.read()
        file_type = imghdr.what(None, h=file_content)
        mime_type, _ = mimetypes.guess_type(file.filename)
        
        if file_type is None and mime_type not in allowed_video_types:
            raise HTTPException(status_code=400, detail="Only image and video files are allowed")
        
        file_path = os.path.join(folder_path, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
    
    return {"status": "Upload success!"}