from fastapi import FastAPI
from app.routers import chat, faqs
from app.database import engine, Base

# Crear las tablas de la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar la aplicación
app = FastAPI(
    title="Chatbot Backend",
    description="Backend para un chatbot que utiliza IA y NLP.",
    version="1.0.0"
)

# Incluir los routers
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(faqs.router, prefix="/faqs", tags=["FAQs"])
