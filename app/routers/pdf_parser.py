from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import shutil
import uuid
import os
from app.utils.pdf_parser import parse_pdf_to_questions
from app.dependencies.dependencies import get_current_user
from app.models.models import AppUser

router = APIRouter(prefix="/pdf", tags=["PDF Parser"])

UPLOAD_DIR = "uploads/pdf"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/parse")
async def parse_pdf(
    file: UploadFile = File(...),
    _: AppUser = Depends(get_current_user),
):
    """
    Upload file PDF và parse ra danh sách câu hỏi JSON.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be PDF")

    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.pdf")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        questions = parse_pdf_to_questions(file_path)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(file_path)
