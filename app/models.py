from sqlalchemy import Column, Integer, String, ARRAY
from app.database import Base

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    keywords = Column(ARRAY(String), nullable=False)
    response = Column(String, nullable=False)
