import spacy

# Cargar el modelo de spaCy
nlp = spacy.load("es_core_news_sm")

def extract_keywords(user_input: str):
    doc = nlp(user_input)
    keywords = [token.text.lower() for token in doc if token.is_alpha]
    return keywords
