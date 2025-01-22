import spacy

nlp = spacy.load("es_core_news_md")

def extract_keywords(user_input: str):
    doc = nlp(user_input)
    keywords = [token.text.lower() for token in doc if token.is_alpha]
    return keywords