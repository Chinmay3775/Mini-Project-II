# ### UPDATED app.py (single best theme, with animated flip cards)

# import streamlit as st
# from flashcard import generate_flashcards, get_flashcard_word_count
# from image_processing import extract_text
# from text_to_speech import text_to_speech
# import random
# import os

# # Page configuration
# st.set_page_config(
#     page_title="Smart Flashcard Generator",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Load CSS
# def local_css(file_name):
#     with open(file_name, "r") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# local_css("styles.css")

# # Initialize session state
# def initialize_state():
#     state_defaults = {
#         'flashcards': {},
#         'current_index': 0,
#         'cards_generated': 0,
#         'texts_processed': 0,
#         'last_shuffle_state': False,
#         'shuffled_keys': [],
#         'input_method': "Text",
#         'text_word_count': 0,
#         'flashcard_word_count': 0,
#         'card_flipped': False
#     }
#     for key, val in state_defaults.items():
#         if key not in st.session_state:
#             st.session_state[key] = val

# initialize_state()

# # --- Header
# st.markdown('<h1 class="main-header">🫠 Smart Flashcard Generator</h1>', unsafe_allow_html=True)

# # --- Sidebar
# with st.sidebar:
#     st.markdown('<h1 class="main-header">Settings</h1>', unsafe_allow_html=True)

#     st.markdown("<h2> 📊 Statistics<h2>",unsafe_allow_html=True)
#     st.markdown(f"""
#         <div class="stats-row">
#             <div class="stat-container">
#                 <div class="stat-value">{st.session_state.text_word_count}</div>
#                 <div class="stat-label">Words in Text</div>
#             </div>
#             <div class="stat-container">
#                 <div class="stat-value">{st.session_state.flashcard_word_count}</div>
#                 <div class="stat-label">Words in Cards</div>
#             </div>
#             <div class="stat-container">
#                 <div class="stat-value">{len(st.session_state.flashcards)}</div>
#                 <div class="stat-label">Current Cards</div>
#             </div>
#             <div class="stat-container">
#                 <div class="stat-value">{st.session_state.texts_processed}</div>
#                 <div class="stat-label">Texts Processed</div>
#             </div>
#             <div class="stat-container">
#                 <div class="stat-value">{st.session_state.cards_generated}</div>
#                 <div class="stat-label">Total Generated</div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# # --- Main Layout
# col1, col2 = st.columns([2, 3])

# with col1:
#     st.radio("Input method:", ["Text", "Image"], key="input_method_selector", horizontal=True)
#     st.session_state.input_method = st.session_state.input_method_selector

#     with st.form(key="input_form"):
#         if st.session_state.input_method == "Text":
#             text_input = st.text_area("Enter your text:", height=150,
#                                       placeholder="Paste your study material here...", key="input_text")
#             submit_button = st.form_submit_button("Generate Flashcards", use_container_width=True)

#             if submit_button:
#                 if text_input.strip():
#                     with st.spinner("Generating flashcards..."):
#                         flashcards = generate_flashcards(text_input)
#                         if flashcards:
#                             st.session_state.flashcards = flashcards
#                             st.session_state.current_index = 0
#                             st.session_state.cards_generated += len(flashcards)
#                             st.session_state.texts_processed += 1
#                             st.session_state.text_word_count = len(text_input.split())
#                             st.session_state.flashcard_word_count = get_flashcard_word_count(flashcards)
#                             st.session_state.card_flipped = False
#                             st.success(f"Generated {len(flashcards)} flashcards!")
#                         else:
#                             st.error("Flashcard generation failed.")
#                 else:
#                     st.warning("Please enter some text!")

#         else:
#             uploaded_file = st.file_uploader("Upload an image containing text", type=["png", "jpg", "jpeg"])
#             submit_button = st.form_submit_button("Extract & Generate Flashcards", use_container_width=True)

#             if submit_button:
#                 if uploaded_file:
#                     with st.spinner("Processing image..."):
#                         image_path = f"temp_{uploaded_file.name}"
#                         with open(image_path, "wb") as f:
#                             f.write(uploaded_file.getbuffer())

#                         extracted_text = extract_text(image_path)
#                         os.remove(image_path)

#                         if extracted_text:
#                             preview = extracted_text[:200] + ("..." if len(extracted_text) > 200 else "")
#                             st.text_area("Extracted text:", value=preview, height=100, disabled=True)

#                             flashcards = generate_flashcards(extracted_text)
#                             if flashcards:
#                                 st.session_state.flashcards = flashcards
#                                 st.session_state.current_index = 0
#                                 st.session_state.cards_generated += len(flashcards)
#                                 st.session_state.texts_processed += 1
#                                 st.session_state.text_word_count = len(extracted_text.split())
#                                 st.session_state.flashcard_word_count = get_flashcard_word_count(flashcards)
#                                 st.session_state.card_flipped = False
#                                 st.success(f"Generated {len(flashcards)} flashcards!")
#                             else:
#                                 st.error("Flashcard generation failed.")
#                         else:
#                             st.error("No text could be extracted from the image.")
#                 else:
#                     st.warning("Please upload an image!")

# # --- Flashcard Display
# with col2:
#     if st.session_state.flashcards:
#         flashcards = st.session_state.flashcards
#         current_index = st.session_state.current_index
#         keys = list(flashcards.keys())
#         values = [flashcards[k] for k in keys]

#         progress = (current_index + 1) / len(flashcards)
#         st.markdown(f"""
#             <div class="progress-container">
#                 <div style="height: 100%; width: {progress * 100}%; background-color: #2563EB;"></div>
#             </div>
#         """, unsafe_allow_html=True)

#         # Get current flashcard content
#         question = f"Point {current_index + 1}"
#         answer = values[current_index]
        
#         # Determine if flipped (add 'card-flipped' class if true)
#         flip_class = "card-flipped" if st.session_state.card_flipped else ""
        
#         # Display flip card with front and back
#         st.markdown(f"""
#             <div class="flip-card {flip_class}">
#               <div class="flip-card-inner">
#                 <div class="flip-card-front">
#                   {question}
#                 </div>
#                 <div class="flip-card-back">
#                   {answer}
#                 </div>
#               </div>
#             </div>
#             <div class="card-counter">{current_index + 1}/{len(flashcards)}</div>
#         """, unsafe_allow_html=True)

#         col_prev, col_flip, col_audio, col_next = st.columns([1, 1, 1, 1])

#         with col_prev:
#             if st.button("⬅️ Previous", disabled=current_index == 0):
#                 st.session_state.current_index -= 1
#                 st.session_state.card_flipped = False
#                 st.rerun()

#         with col_flip:
#             if st.button("🔄 Flip Card"):
#                 st.session_state.card_flipped = not st.session_state.card_flipped
#                 # st.rerun()  # Added rerun to make flip effect more responsive

#         with col_audio:
#             if st.button("🔊 Read Aloud"):
#                 with st.spinner("Converting to speech..."):
#                     text_to_speech(values[current_index])
#                     st.success("Audio saved")

#         with col_next:
#             if st.button("Next ➡️", disabled=current_index == len(flashcards) - 1):
#                 st.session_state.current_index += 1
#                 st.session_state.card_flipped = False
#                 st.rerun()

#     else:
#         st.markdown("""
#             <div class="empty-state">
#                 <h2>No Flashcards Yet</h2>
#                 <p>Enter your study material or upload an image to generate AI-powered flashcards.</p>
#             </div>
#         """, unsafe_allow_html=True)

# # --- Footer
# st.markdown("""
#     <div class="footer">
#         Smart Flashcard Generator • Powered by AI<br>
#         © Chinmay Keripale, Asim Kazi & Aditya Kulkarni
#     </div>
# """, unsafe_allow_html=True)


###############################################################################

import streamlit as st
import re
from gtts import gTTS
import tempfile
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page configuration
st.set_page_config(
    page_title="Smart Flashcard Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to top left, #0f172a, #1e293b, #334155);
    color: #e2e8f0;
}

.flip-card {
    background-color: transparent;
    width: 100%;
    height: 250px;
    perspective: 1000px;
    margin: 20px 0;
}

.flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.8s;
    transform-style: preserve-3d;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.card-flipped .flip-card-inner {
    transform: rotateY(180deg);
}

.flip-card-front, .flip-card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    padding: 25px;
    box-sizing: border-box;
    overflow-y: auto;
}

.flip-card-front {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    color: #60a5fa;
    font-size: 1.4rem;
    font-weight: 600;
    border-left: 6px solid #3b82f6;
}

.flip-card-back {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    color: #f8fafc;
    transform: rotateY(180deg);
    font-size: 1.1rem;
    line-height: 1.6;
    border-left: 6px solid #60a5fa;
}

.progress-container {
    width: 100%;
    height: 8px;
    background-color: #475569;
    border-radius: 6px;
    margin-bottom: 20px;
    overflow: hidden;
}

.stats-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 0.75rem;
}

.stat-container {
    background-color: #1e293b;
    padding: 1rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.2);
}

.stat-value {
    font-size: 1.4rem;
    font-weight: 600;
    color: #3b82f6;
}

.stat-label {
    font-size: 0.95rem;
    color: #cbd5e1;
}

.main-header {
    text-align: center;
    font-size: 2.8rem;
    font-weight: 700;
    color: #60a5fa;
    margin: 1rem 0 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_state():
    state_defaults = {
        'flashcards': {},
        'current_index': 0,
        'cards_generated': 0,
        'texts_processed': 0,
        'text_word_count': 0,
        'flashcard_word_count': 0,
        'card_flipped': False
    }
    for key, val in state_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

initialize_state()

# Your original text processing logic (simplified)
def normalize_text(text):
    # Remove IPA pronunciation (anything between slashes)
    text = re.sub(r'/[^/]+/', '', text)
    # Remove pronunciation in brackets
    text = re.sub(r'\[[^\]]+\]', '', text)
    # Remove language tags like 'Marathi: Mumbai,'
    text = re.sub(r'\b\w+:\s*[^,;()]+[,;)]?', '', text)
    # Remove special characters
    text = re.sub(r'["""]', '', text)
    # Remove extra spaces and fix spacing around punctuation
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([,.])', r'\1', text)
    # Remove leftover empty parentheses
    text = re.sub(r'\(\s*[.,;:]*\s*\)', '', text)
    return text.strip()

def extract_keyphrases_simple(text, top_n=10):
    """Simple keyword extraction using TF-IDF"""
    try:
        # Simple sentence splitting
        sentences = [sent.strip() for sent in re.split(r'[.!?]+', text) if sent.strip()]
        
        if len(sentences) < 2:
            return text.split()[:top_n]
        
        # Use TF-IDF for keyword extraction
        vectorizer = TfidfVectorizer(
            max_features=top_n,
            stop_words='english',
            ngram_range=(1, 2),
            max_df=0.8,
            min_df=1
        )
        
        tfidf_matrix = vectorizer.fit_transform(sentences)
        feature_names = vectorizer.get_feature_names_out()
        
        # Get average TF-IDF scores
        mean_scores = np.mean(tfidf_matrix.toarray(), axis=0)
        keyword_scores = [(feature_names[i], mean_scores[i]) for i in range(len(feature_names))]
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [kw[0] for kw in keyword_scores]
    except Exception as e:
        st.error(f"Keyword extraction error: {e}")
        return text.split()[:top_n]

def find_relevant_sentences_simple(text, keyphrases, top_sentences=1):
    """Find sentences most relevant to keyphrases using simple matching"""
    try:
        sentences = [sent.strip() for sent in re.split(r'[.!?]+', text) if sent.strip() and len(sent.strip()) > 20]
        
        if not sentences:
            return [text]
        
        # Score sentences based on keyword presence
        sentence_scores = []
        for sentence in sentences:
            score = 0
            sentence_lower = sentence.lower()
            for phrase in keyphrases:
                if phrase.lower() in sentence_lower:
                    score += 1 + len(phrase.split())  # Longer phrases get more weight
            sentence_scores.append((sentence, score))
        
        # Sort by score and take top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_sentences = []
        for sentence, score in sentence_scores:
            if sentence not in seen and score > 0:
                unique_sentences.append(sentence)
                seen.add(sentence)
        
        return unique_sentences[:min(len(keyphrases), len(unique_sentences))] or sentences[:5]
    
    except Exception as e:
        st.error(f"Sentence extraction error: {e}")
        sentences = text.split('.')
        return [s.strip() + '.' for s in sentences if s.strip()][:5]

def generate_flashcards(text, top_n=10):
    """Your original flashcard generation logic (simplified)"""
    try:
        normalized_text = normalize_text(text)
        keyphrases = extract_keyphrases_simple(normalized_text, top_n=top_n)
        sentences = find_relevant_sentences_simple(normalized_text, keyphrases, top_sentences=1)
        return {f"Card {i+1}": sent + ('.' if not sent.endswith('.') else '') for i, sent in enumerate(sentences)}
    except Exception as e:
        st.error(f"Flashcard generation error: {e}")
        return {}

def get_flashcard_word_count(flashcards):
    """Returns total number of words across all flashcards"""
    return sum(len(card.split()) for card in flashcards.values())

def text_to_speech(text):
    """Convert text to speech"""
    try:
        tts = gTTS(text=text, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tts.save(tmp_file.name)
            return tmp_file.name
    except Exception as e:
        st.error(f"Audio generation failed: {e}")
        return None

# Header
st.markdown('<h1 class="main-header">🧠 Smart Flashcard Generator</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<h1 class="main-header">Settings</h1>', unsafe_allow_html=True)
    
    st.markdown("<h2>📊 Statistics<h2>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="stats-row">
            <div class="stat-container">
                <div class="stat-value">{st.session_state.text_word_count}</div>
                <div class="stat-label">Words in Text</div>
            </div>
            <div class="stat-container">
                <div class="stat-value">{st.session_state.flashcard_word_count}</div>
                <div class="stat-label">Words in Cards</div>
            </div>
            <div class="stat-container">
                <div class="stat-value">{len(st.session_state.flashcards)}</div>
                <div class="stat-label">Current Cards</div>
            </div>
            <div class="stat-container">
                <div class="stat-value">{st.session_state.texts_processed}</div>
                <div class="stat-label">Texts Processed</div>
            </div>
            <div class="stat-container">
                <div class="stat-value">{st.session_state.cards_generated}</div>
                <div class="stat-label">Total Generated</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Main Layout
col1, col2 = st.columns([2, 3])

with col1:
    with st.form(key="input_form"):
        text_input = st.text_area("Enter your text:", height=150,
                                  placeholder="Paste your study material here...", key="input_text")
        submit_button = st.form_submit_button("Generate Flashcards", use_container_width=True)

        if submit_button:
            if text_input.strip():
                with st.spinner("Generating flashcards..."):
                    flashcards = generate_flashcards(text_input)
                    if flashcards:
                        st.session_state.flashcards = flashcards
                        st.session_state.current_index = 0
                        st.session_state.cards_generated += len(flashcards)
                        st.session_state.texts_processed += 1
                        st.session_state.text_word_count = len(text_input.split())
                        st.session_state.flashcard_word_count = get_flashcard_word_count(flashcards)
                        st.session_state.card_flipped = False
                        st.success(f"Generated {len(flashcards)} flashcards!")
                    else:
                        st.error("Flashcard generation failed.")
            else:
                st.warning("Please enter some text!")

# Flashcard Display
with col2:
    if st.session_state.flashcards:
        flashcards = st.session_state.flashcards
        current_index = st.session_state.current_index
        keys = list(flashcards.keys())
        values = [flashcards[k] for k in keys]

        progress = (current_index + 1) / len(flashcards)
        st.markdown(f"""
            <div class="progress-container">
                <div style="height: 100%; width: {progress * 100}%; background-color: #2563EB;"></div>
            </div>
        """, unsafe_allow_html=True)

        # Flip card
        question = f"Point {current_index + 1}"
        answer = values[current_index]
        
        flip_class = "card-flipped" if st.session_state.card_flipped else ""
        
        st.markdown(f"""
            <div class="flip-card {flip_class}">
              <div class="flip-card-inner">
                <div class="flip-card-front">
                  {question}
                </div>
                <div class="flip-card-back">
                  {answer}
                </div>
              </div>
            </div>
            <div class="card-counter" style="text-align: center; color: #94a3b8; margin-top: 10px;">
                {current_index + 1}/{len(flashcards)}
            </div>
        """, unsafe_allow_html=True)

        col_prev, col_flip, col_audio, col_next = st.columns([1, 1, 1, 1])

        with col_prev:
            if st.button("⬅️ Previous", disabled=current_index == 0):
                st.session_state.current_index -= 1
                st.session_state.card_flipped = False
                st.rerun()

        with col_flip:
            if st.button("🔄 Flip Card"):
                st.session_state.card_flipped = not st.session_state.card_flipped
                st.rerun()

        with col_audio:
            if st.button("🔊 Read Aloud"):
                audio_file = text_to_speech(values[current_index])
                if audio_file and os.path.exists(audio_file):
                    with open(audio_file, "rb") as f:
                        st.audio(f.read())
                    os.unlink(audio_file)

        with col_next:
            if st.button("Next ➡️", disabled=current_index == len(flashcards) - 1):
                st.session_state.current_index += 1
                st.session_state.card_flipped = False
                st.rerun()

    else:
        st.markdown("""
            <div class="empty-state" style="
                text-align: center;
                padding: 6rem 4rem;
                background-color: #1e293b;
                border: 1px dashed #64748b;
                border-radius: 12px;
                margin-top: 2rem;
            ">
                <h2 style="color: #3b82f6;">No Flashcards Yet</h2>
                <p style="color: #cbd5e1;">Enter your study material to generate AI-powered flashcards.</p>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="
        text-align: center;
        font-size: 0.9rem;
        color: #94a3b8;
        margin-top: 2rem;
        padding-top: 0.75rem;
        border-top: 1px solid #334155;
    ">
        Smart Flashcard Generator • Powered by AI<br>
        © Chinmay Keripale, Asim Kazi & Aditya Kulkarni
    </div>
""", unsafe_allow_html=True)