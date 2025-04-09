import spacy
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

def preprocess_text(text):
    """Splits text into sentences while maintaining structure and meaning."""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    return sentences

def determine_flashcard_count(text):
    """Determines the number of flashcards based on text length."""
    word_count = len(text.split())
    if word_count < 100:
        return 3
    elif 100 <= word_count < 300:
        return 5
    elif 300 <= word_count < 600:
        return 7
    else:
        return 10

def generate_flashcards(text):
    """Generates clear, concise, and meaningful flashcards (2–3 sentence max each)."""
    num_flashcards = determine_flashcard_count(text)
    sentences = preprocess_text(text)

    if not sentences:
        return {}

    # Generate sentence embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(sentences)
    similarity_matrix = cosine_similarity(embeddings)
    
    # TextRank graph
    graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(graph)

    # Sort sentences by score
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    selected = []
    used_phrases = set()

    for _, sentence in ranked_sentences:
        if len(selected) >= num_flashcards:
            break
        cleaned = sentence.strip()
        if cleaned and cleaned not in used_phrases:
            # Limit to 2–3 short sentences
            trimmed = '. '.join(cleaned.split('. ')[:3]).strip()
            if not trimmed.endswith('.'):
                trimmed += '.'
            selected.append(trimmed)
            used_phrases.add(trimmed)

    # Format as numbered flashcards
    flashcards = {f"Point {i+1}": point for i, point in enumerate(selected)}
    return flashcards
