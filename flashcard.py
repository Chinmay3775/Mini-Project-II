import re
from keybert import KeyBERT
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load models only once
nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT('all-MiniLM-L6-v2')
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def normalize_text(text):
    # Remove IPA pronunciation (anything between slashes, e.g., /mʊmˈbaɪ/)
    text = re.sub(r'/[^/]+/', '', text)
    
    # Remove pronunciation in brackets, e.g. [ˈmumbəi]
    text = re.sub(r'\[[^\]]+\]', '', text)
    
    # Remove language tags like 'Marathi: Mumbaī,' or 'Hindi: ...'
    text = re.sub(r'\b\w+:\s*[^,;()]+[,;)]?', '', text)
    
    # Remove special characters like ⓘ or others
    text = re.sub(r'[ⓘ]', '', text)
    
    # Remove extra spaces and fix spacing around punctuation
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([,.])', r'\1', text)
    
    # Remove leftover empty parentheses or parentheses with only spaces/punctuation
    text = re.sub(r'\(\s*[.,;:]*\s*\)', '', text)
    
    return text.strip()

def extract_keyphrases(text, top_n=10):
    keyphrases = kw_model.extract_keywords(text, top_n=20, stop_words='english')
    return [kp[0] for kp in keyphrases]

def find_relevant_sentences(text, keyphrases, top_sentences=1):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    
    sentence_embs = embed_model.encode(sentences)
    keyphrase_embs = embed_model.encode(keyphrases)

    flashcards = []
    for i, kp_emb in enumerate(keyphrase_embs):
        sims = cosine_similarity([kp_emb], sentence_embs)[0]
        top_idx = sims.argsort()[-top_sentences:][::-1]
        for idx in top_idx:
            flashcards.append(sentences[idx])

    # Remove duplicates while preserving order
    seen = set()
    unique_flashcards = []
    for f in flashcards:
        if f not in seen:
            unique_flashcards.append(f)
            seen.add(f)
    return unique_flashcards

def generate_flashcards(text, top_n=10):
    """Returns a dictionary: {'Card 1': sentence, 'Card 2': sentence, ...}"""
    normalized_text = normalize_text(text)  # Normalize before processing
    keyphrases = extract_keyphrases(normalized_text, top_n=top_n)
    sentences = find_relevant_sentences(normalized_text, keyphrases, top_sentences=1)
    return {f"Card {i+1}": sent for i, sent in enumerate(sentences)}

def get_flashcard_word_count(flashcards):
    """Returns total number of words across all flashcards"""
    return sum(len(card.split()) for card in flashcards.values())
