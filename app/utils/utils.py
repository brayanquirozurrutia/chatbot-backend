import os
import requests
from dotenv import load_dotenv

load_dotenv()
WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE")

def generate_whatsapp_link(message: str) -> str:
    """
    Generate a WhatsApp link with a given message using inline styles.
    :param message: The message to include in the link.
    :return: The formatted WhatsApp link with inline styles.
    """
    whatsapp_link = f"https://wa.me/{WHATSAPP_PHONE}?text={requests.utils.quote(message)}"
    return (
        f"👉 <a href='{whatsapp_link}' target='_blank' style='"
        f"color: #2563eb; text-decoration: underline; transition: color 0.2s ease-in-out;' "
        f"onmouseover=\"this.style.color='#1d4ed8';\" onmouseout=\"this.style.color='#2563eb';\">"
        "Contáctame por WhatsApp</a>"
    )
