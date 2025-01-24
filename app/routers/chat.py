from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.chat_ai import generate_response
from app.services.nlp import extract_keywords
from app.services.redis_cache import get_cache, set_cache
from app.utils.utils import generate_whatsapp_link

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
    """
    Search for the most relevant FAQ response based on the keywords extracted from the user input.
    :param db: The database session
    :param keywords: The keywords extracted from the user input
    :return: The most relevant FAQ response or a default message
    """
    from sqlalchemy import text

    keywords_lower = [keyword.lower() for keyword in keywords]

    sql = text(
        """
        SELECT id, question, keywords, response,
            (SELECT COUNT(*) FROM unnest(faqs.keywords) AS keyword WHERE keyword = ANY(:keywords)) AS match_count
        FROM faqs
        ORDER BY match_count DESC
        LIMIT 1
        """
    )

    result = db.execute(sql, {"keywords": keywords_lower}).fetchone()

    if result and result[4] >= 2:
        return result[3]

    whatsapp_message = "Hola, Brayan. Me gustaría obtener más información."
    return (
        "Lo siento, no tengo una respuesta exacta para esa pregunta. "
        "Te invito a revisar nuestras preguntas frecuentes o, si prefieres, contáctame directamente por WhatsApp.\n\n"
        f"{generate_whatsapp_link(whatsapp_message)}"
    )
