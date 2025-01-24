import logging
import os
import requests
import json
from dotenv import load_dotenv
from app.utils.utils import generate_whatsapp_link

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

logger = logging.getLogger(__name__)

def generate_response(user_input: str, faq_base_response: str = None) -> str:
    """
    Generate a response using the Gemini API
    :param user_input: The user input
    :param faq_base_response: The base response from the FAQ
    :return: The generated response
    """
    try:
        if faq_base_response:
            prompt = (
                f"Tienes una respuesta base:\n"
                f"{faq_base_response}\n\n"
                f"Por favor, expande esta respuesta de forma detallada, amigable y profesional. "
                f"Mantén el contexto y no cambies el significado original. "
                f"Formula tu respuesta de forma clara y concisa en un lenguaje natural con un máximo de 500 caracteres."
            )
        else:
            prompt = user_input

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            data=json.dumps(payload),
        )

        if response.status_code == 200:
            data = response.json()

            generated_content = (
                data.get("candidates", [])[0]
                .get("content", {})
                .get("parts", [])[0]
                .get("text", "")
            )

            if "contáctanos" in generated_content.lower() or "ponte en contacto" in generated_content.lower():
                whatsapp_message = "Hola, Brayan. Me gustaría obtener más información sobre tus servicios."
                generated_content += f"\n\n{generate_whatsapp_link(whatsapp_message)}"

            return generated_content.strip()
        else:
            logger.error(f"Error en la API de Gemini: {response.status_code}, {response.text}")
            return "Lo siento, no puedo procesar tu solicitud en este momento."
    except Exception as e:
        logger.exception(f"Error al generar respuesta: {e}")
        return "Lo siento, no puedo procesar tu solicitud en este momento."