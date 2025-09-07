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

# Page configuration
st.set_page_config(
    page_title="Smart Flashcard Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for flip cards
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
}

.flip-card-front {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-size: 1.4rem;
    font-weight: 600;
}

.flip-card-back {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    transform: rotateY(180deg);
    font-size: 1.1rem;
    line-height: 1.6;
    overflow-y: auto;
}

.progress-container {
    width: 100%;
    height: 8px;
    background-color: #475569;
    border-radius: 6px;
    margin-bottom: 20px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea, #764ba2);
    transition: width 0.3s ease;
}

.stats-container {
    background: rgba(30, 41, 59, 0.8);
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}

.stat-item {
    display: flex;
    justify-content: space-between;
    margin: 5px 0;
    color: #cbd5e1;
}

.stat-value {
    color: #60a5fa;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = {}
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'card_flipped' not in st.session_state:
    st.session_state.card_flipped = False
if 'cards_generated' not in st.session_state:
    st.session_state.cards_generated = 0
if 'texts_processed' not in st.session_state:
    st.session_state.texts_processed = 0

def clean_text(text):
    """Clean and normalize text"""
    text = re.sub(r'\s+', ' ', text.strip())
    text = re.sub(r'["""]', '', text)
    return text

def generate_flashcards(text, max_cards=10):
    """Generate flashcards with improved logic"""
    text = clean_text(text)
    
    # Split by sentences and clean
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    # Filter out very short or very long sentences
    good_sentences = []
    for sentence in sentences:
        word_count = len(sentence.split())
        if 5 <= word_count <= 30:  # Good length for flashcards
            good_sentences.append(sentence)
    
    # Take the best sentences
    good_sentences = good_sentences[:max_cards]
    
    return {f"Point {i+1}": sentence + "." for i, sentence in enumerate(good_sentences)}

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
st.markdown('<h1 style="text-align: center; color: #60a5fa; margin-bottom: 30px;">🧠 Smart Flashcard Generator</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    st.markdown("### 📊 Statistics")
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-item">
            <span>Cards Generated:</span>
            <span class="stat-value">{st.session_state.cards_generated}</span>
        </div>
        <div class="stat-item">
            <span>Texts Processed:</span>
            <span class="stat-value">{st.session_state.texts_processed}</span>
        </div>
        <div class="stat-item">
            <span>Current Cards:</span>
            <span class="stat-value">{len(st.session_state.flashcards)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([2, 3])

with col1:
    st.markdown("### 📝 Input Your Text")
    
    with st.form("flashcard_form"):
        text_input = st.text_area(
            "Enter your study material:",
            height=200,
            placeholder="Paste your study material here..."
        )
        
        num_cards = st.slider("Number of flashcards:", 3, 15, 8)
        
        if st.form_submit_button("🚀 Generate Flashcards", use_container_width=True):
            if text_input.strip():
                with st.spinner("Generating flashcards..."):
                    flashcards = generate_flashcards(text_input, num_cards)
                    if flashcards:
                        st.session_state.flashcards = flashcards
                        st.session_state.current_index = 0
                        st.session_state.card_flipped = False
                        st.session_state.cards_generated += len(flashcards)
                        st.session_state.texts_processed += 1
                        st.success(f"Generated {len(flashcards)} flashcards!")
                    else:
                        st.error("Could not generate flashcards from this text.")
            else:
                st.warning("Please enter some text!")

with col2:
    if st.session_state.flashcards:
        flashcards = st.session_state.flashcards
        current_index = st.session_state.current_index
        
        keys = list(flashcards.keys())
        values = list(flashcards.values())
        
        # Progress bar
        progress = (current_index + 1) / len(flashcards)
        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-fill" style="width: {progress * 100}%;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Flip card
        flip_class = "card-flipped" if st.session_state.card_flipped else ""
        
        st.markdown(f"""
        <div class="flip-card {flip_class}">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    {keys[current_index]}
                </div>
                <div class="flip-card-back">
                    {values[current_index]}
                </div>
            </div>
        </div>
        <div style="text-align: center; color: #94a3b8; margin-top: 10px;">
            {current_index + 1} / {len(flashcards)}
        </div>
        """, unsafe_allow_html=True)
        
        # Controls
        col_prev, col_flip, col_audio, col_next = st.columns([1, 1, 1, 1])
        
        with col_prev:
            if st.button("⬅️ Previous", disabled=current_index == 0):
                st.session_state.current_index -= 1
                st.session_state.card_flipped = False
                st.rerun()
        
        with col_flip:
            if st.button("🔄 Flip"):
                st.session_state.card_flipped = not st.session_state.card_flipped
                st.rerun()
        
        with col_audio:
            if st.button("🔊 Audio"):
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
        <div style="
            text-align: center;
            padding: 60px 40px;
            background: rgba(30, 41, 59, 0.5);
            border: 2px dashed #64748b;
            border-radius: 15px;
            margin-top: 40px;
        ">
            <h3 style="color: #60a5fa; margin-bottom: 15px;">No Flashcards Yet</h3>
            <p style="color: #cbd5e1;">Enter your study material on the left to generate AI-powered flashcards.</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="
    text-align: center;
    margin-top: 50px;
    padding-top: 20px;
    border-top: 1px solid #334155;
    color: #94a3b8;
">
    Smart Flashcard Generator • Powered by AI<br>
    © Your Name Here
</div>
""", unsafe_allow_html=True)