import spacy

nlp = spacy.load("es_core_news_md")

def extract_keywords(user_input: str) -> list[str]:
    """
    Extract relevant keywords from the user input.
    :param user_input: The user inputs
    :return: The relevant keywords
    """
    doc = nlp(user_input)

    keywords = [
        token.text.lower()
        for token in doc
        if token.is_alpha and token.pos_ in {"NOUN", "VERB", "ADJ", "ADV"}
    ]
    return keywords