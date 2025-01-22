from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FAQ

router = APIRouter()

class FAQRequest(BaseModel):
    question: str
    keywords: List[str]
    response: str

@router.post("/", summary="Agregar una nueva FAQ")
def add_faq(faq_data: FAQRequest, db: Session = Depends(get_db)):
    faq = FAQ(
        question=faq_data.question,
        keywords=faq_data.keywords,
        response=faq_data.response
    )
    db.add(faq)
    db.commit()
    db.refresh(faq)
    return {"message": "FAQ agregada exitosamente!", "faq": faq}

@router.get("/", summary="Obtener todas las FAQs")
def get_all_faqs(db: Session = Depends(get_db)):
    return db.query(FAQ).all()
