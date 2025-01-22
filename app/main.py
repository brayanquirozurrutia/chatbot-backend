import logging

from fastapi import FastAPI
from app.routers import chat, faqs, cache
from app.database import engine, Base

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Chatbot Backend",
    description="Backend para un chatbot que utiliza IA y NLP.",
    version="1.0.0"
)

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(faqs.router, prefix="/faqs", tags=["FAQs"])
app.include_router(cache.router, prefix="/cache", tags=["Caché"])
