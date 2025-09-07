import re
from keybert import KeyBERT
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import subprocess
import sys
import os

# Function to download spacy model if not available
def download_spacy_model():
    try:
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except OSError:
        print("Downloading spaCy English model...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        nlp = spacy.load("en_core_web_sm")
        return nlp

# Load models only once with error handling
try:
    nlp = download_spacy_model()
    kw_model = KeyBERT('all-MiniLM-L6-v2')
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading models: {e}")
    # Fallback - create dummy objects to prevent import errors
    nlp = None
    kw_model = None
    embed_model = None

def normalize_text(text):
    # Remove IPA pronunciation (anything between slashes, e.g., /mʊmˈbaɪ/)
    text = re.sub(r'/[^/]+/', '', text)
    
    # Remove pronunciation in brackets, e.g. [ˈmumbəi]
    text = re.sub(r'\[[^\]]+\]', '', text)
    
    # Remove language tags like 'Marathi: Mumbaī,' or 'Hindi: ...'
    text = re.sub(r'\b\w+:\s*[^,;()]+[,;)]?', '', text)
    
    # Remove special characters like " or others
    text = re.sub(r'[""]', '', text)
    
    # Remove extra spaces and fix spacing around punctuation
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([,.])', r'\1', text)
    
    # Remove leftover empty parentheses or parentheses with only spaces/punctuation
    text = re.sub(r'\(\s*[.,;:]*\s*\)', '', text)
    
    return text.strip()

def extract_keyphrases(text, top_n=10):
    if kw_model is None:
        # Fallback: simple keyword extraction
        words = text.split()
        return words[:min(top_n, len(words))]
    
    try:
        keyphrases = kw_model.extract_keywords(text, top_n=20, stop_words='english')
        return [kp[0] for kp in keyphrases]
    except Exception as e:
        print(f"Error extracting keyphrases: {e}")
        words = text.split()
        return words[:min(top_n, len(words))]

def find_relevant_sentences(text, keyphrases, top_sentences=1):
    if nlp is None or embed_model is None:
        # Fallback: simple sentence splitting
        sentences = text.split('.')
        sentences = [s.strip() + '.' for s in sentences if s.strip()]
        return sentences[:min(len(sentences), len(keyphrases))]
    
    try:
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
    except Exception as e:
        print(f"Error finding relevant sentences: {e}")
        # Fallback
        sentences = text.split('.')
        sentences = [s.strip() + '.' for s in sentences if s.strip()]
        return sentences[:min(len(sentences), len(keyphrases))]

def generate_flashcards(text, top_n=10):
    """Returns a dictionary: {'Card 1': sentence, 'Card 2': sentence, ...}"""
    try:
        normalized_text = normalize_text(text)
        keyphrases = extract_keyphrases(normalized_text, top_n=top_n)
        sentences = find_relevant_sentences(normalized_text, keyphrases, top_sentences=1)
        return {f"Card {i+1}": sent for i, sent in enumerate(sentences)}
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        # Very simple fallback
        sentences = text.split('.')
        sentences = [s.strip() + '.' for s in sentences if s.strip() and len(s.strip()) > 10]
        return {f"Card {i+1}": sent for i, sent in enumerate(sentences[:10])}

def get_flashcard_word_count(flashcards):
    """Returns total number of words across all flashcards"""
    try:
        return sum(len(card.split()) for card in flashcards.values())
    except Exception:
        return 0