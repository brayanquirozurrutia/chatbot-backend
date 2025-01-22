import os

import requests
from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.chat_ai import generate_response
from app.services.nlp import extract_keywords
from app.models import FAQ
from app.services.redis_cache import get_cache, set_cache
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE")

router = APIRouter()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            user_message = await websocket.receive_text()

            cached_response = await get_cache(user_message)
            if cached_response:
                await websocket.send_text(cached_response)
                continue

            greeting_response = handle_greetings(user_message)
            if greeting_response:
                await websocket.send_text(greeting_response)
                continue

            keywords = extract_keywords(user_message)
            faq_response = find_faq_response(db, keywords)

            if "Lo siento" in faq_response:
                response = faq_response
            else:
                response = generate_response(user_message, faq_response)

            await set_cache(user_message, response)

            await websocket.send_text(response)
    except Exception as e:
        print(f"Error en el WebSocket: {e}")
        await websocket.close()

def handle_greetings(user_input: str) -> str:
    greetings = [
        "hola",
        "buenos días",
        "buenas tardes",
        "buenas noches",
        "qué tal",
        "cómo estás",
        "hey",
    ]
    if any(greet in user_input.lower() for greet in greetings):
        return "¡Hola! Soy el asistente virtual de Brayan Quiroz. ¿En qué puedo ayudarte hoy?"
    return None

def find_faq_response(db: Session, keywords: list[str]) -> str:
    faqs = db.query(FAQ).all()
    for faq in faqs:
        if set(keywords) & set(faq.keywords):
            return faq.response

    whatsapp_message = "Hola, Brayan. Me gustaría obtener más información."
    whatsapp_link = f"https://wa.me/{WHATSAPP_PHONE}?text={requests.utils.quote(whatsapp_message)}"
    return (
        "Lo siento, no tengo una respuesta exacta para esa pregunta. "
        "Te invito a revisar nuestras preguntas frecuentes o, si prefieres, contáctame directamente por WhatsApp.\n\n"
        f"👉 [Contáctame por WhatsApp]({whatsapp_link})"
    )
