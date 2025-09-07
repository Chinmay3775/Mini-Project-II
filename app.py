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
    layout="wide"
)

# Initialize session state
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = {}
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

def clean_text(text):
    """Clean and normalize text"""
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def simple_generate_flashcards(text, max_cards=10):
    """Generate flashcards using simple text processing"""
    text = clean_text(text)
    
    # Split by sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 15]
    
    # Take meaningful sentences
    sentences = sentences[:max_cards]
    
    return {f"Card {i+1}": sentence + "." for i, sentence in enumerate(sentences)}

def text_to_speech(text):
    """Convert text to speech and return audio file"""
    try:
        tts = gTTS(text=text, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tts.save(tmp_file.name)
            return tmp_file.name
    except Exception as e:
        st.error(f"Audio generation failed: {e}")
        return None

# Header
st.title("🧠 Smart Flashcard Generator")

# Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Input")
    
    with st.form("text_form"):
        text_input = st.text_area(
            "Enter your study material:",
            height=200,
            placeholder="Paste your text here..."
        )
        
        num_cards = st.slider("Number of cards:", 1, 15, 8)
        
        if st.form_submit_button("Generate Flashcards"):
            if text_input.strip():
                with st.spinner("Generating flashcards..."):
                    flashcards = simple_generate_flashcards(text_input, num_cards)
                    st.session_state.flashcards = flashcards
                    st.session_state.current_index = 0
                    st.success(f"Generated {len(flashcards)} flashcards!")
            else:
                st.warning("Please enter some text!")

with col2:
    if st.session_state.flashcards:
        flashcards = st.session_state.flashcards
        current_index = st.session_state.current_index
        
        keys = list(flashcards.keys())
        values = list(flashcards.values())
        
        # Progress
        progress = (current_index + 1) / len(flashcards)
        st.progress(progress, text=f"Card {current_index + 1} of {len(flashcards)}")
        
        # Display card
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin: 20px 0;
            min-height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        ">
            <div style="font-size: 1.2em; line-height: 1.6;">
                {values[current_index]}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Controls
        col_prev, col_audio, col_next = st.columns([1, 1, 1])
        
        with col_prev:
            if st.button("⬅️ Previous", disabled=current_index == 0):
                st.session_state.current_index -= 1
                st.rerun()
        
        with col_audio:
            if st.button("🔊 Audio"):
                audio_file = text_to_speech(values[current_index])
                if audio_file and os.path.exists(audio_file):
                    with open(audio_file, "rb") as f:
                        st.audio(f.read())
                    os.unlink(audio_file)  # Clean up temp file
        
        with col_next:
            if st.button("Next ➡️", disabled=current_index == len(flashcards) - 1):
                st.session_state.current_index += 1
                st.rerun()
                
        # Stats
        with st.sidebar:
            st.metric("Total Cards", len(flashcards))
            st.metric("Current Position", current_index + 1)
            st.metric("Words in Current Card", len(values[current_index].split()))
            
    else:
        st.info("👈 Enter text to generate flashcards")

st.markdown("---")
st.caption("Smart Flashcard Generator")