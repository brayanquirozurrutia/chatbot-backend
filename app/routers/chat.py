from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.nlp import extract_keywords
from app.models import FAQ
from app.services.redis_cache import get_cache, set_cache

router = APIRouter()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            user_message = await websocket.receive_text()

            # Verificar caché para evitar procesamiento redundante
            cached_response = await get_cache(user_message)
            if cached_response:
                await websocket.send_text(cached_response)
                continue

            keywords = extract_keywords(user_message)
            response = find_faq_response(db, keywords)

            # Guardar respuesta en caché
            await set_cache(user_message, response)

            await websocket.send_text(response)
    except Exception as e:
        await websocket.close()

def find_faq_response(db: Session, keywords: list[str]):
    faqs = db.query(FAQ).all()
    for faq in faqs:
        if set(keywords) & set(faq.keywords):
            return faq.response
    return "Lo siento, no tengo una respuesta para esa pregunta."
