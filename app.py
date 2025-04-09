import streamlit as st
from flashcard import generate_flashcards
from image_processing import extract_text
from text_to_speech import text_to_speech
import random

# Page configuration
st.set_page_config(
    page_title="Smart Flashcard Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with improved radio button styling and better contrast
st.markdown("""
    <style>
        /* Main Elements */
        .main {
            background-color: #f8f9fa;
            padding: 2rem;
        }
        
        /* Header Styling */
        .header-container {
            text-align: center;
            padding: 1rem 0 2rem 0;
            border-bottom: 1px solid #e9ecef;
            margin-bottom: 2rem;
        }
        
        .logo-text {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1a202c;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: #2d3748;
            font-weight: 400;
        }
        
        /* Card Styling */
        .flashcard-container {
            width: 100%;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .flashcard {
            width: 100%;
            min-height: 350px;
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            padding: 2rem;
            margin: 1rem 0;
            position: relative;
            overflow-y: auto;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .flashcard:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
        }
        
        .card-content {
            font-size: 1.25rem;
            line-height: 1.6;
            color: #1a202c;
        }
        
        .card-counter {
            position: absolute;
            bottom: 15px;
            right: 15px;
            background-color: #e9ecef;
            color: #1a202c;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }
        
        /* Buttons */
        .nav-button {
            background-color: #2b6cb0;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s;
            width: 120px;
            text-align: center;
        }
        
        .nav-button:hover {
            background-color: #1a4a8c;
        }
        
        .nav-button:disabled {
            background-color: #a0aec0;
            color: #e2e8f0;
            cursor: not-allowed;
        }
        
        .speech-button {
            background-color: #2f855a;
            width: 150px;
        }
        
        .speech-button:hover {
            background-color: #22543d;
        }
        
        /* Form Styling */
        .form-container {
            background-color: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        }
        
        /* Input method selection styling with better contrast */
        .input-method-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #1a202c;
            margin-bottom: 0.75rem;
        }
        
        /* Remove default Streamlit radio styling */
        .stRadio > div {
            background-color: transparent !important;
        }
        
        /* Create custom radio button styling with better contrast */
        .stRadio > div > div {
            background-color: #f0f4f8 !important; /* Light blue background */
            border: 1px solid #90cdf4 !important;
            border-radius: 8px !important;
            margin-bottom: 0.5rem !important;
            padding: 0.5rem !important;
        }
        
        /* Improve text visibility */
        .stRadio > div > div > label {
            color: #1a365d !important; /* Dark blue text */
            font-weight: 600 !important;
        }
        
        .stRadio > div > div:hover {
            border-color: #2b6cb0 !important;
            background-color: #ebf8ff !important; /* Lighter blue on hover */
        }
        
        /* Selected radio button with even better contrast */
        .stRadio > div > div[data-baseweb="radio"] > div:first-child {
            background-color: #2b6cb0 !important; /* Blue dot */
        }
        
        /* Checkbox styling */
        .stCheckbox > div > div > div {
            background-color: #f0f4f8 !important;
        }
        
        .stTextArea > div > div {
            border-radius: 10px !important;
            border: 1px solid #e2e8f0 !important;
        }
        
        .stTextArea > div > div:focus-within {
            border-color: #2b6cb0 !important;
            box-shadow: 0 0 0 1px #2b6cb0 !important;
        }
        
        .submit-btn {
            background-color: #2b6cb0 !important;
            color: white !important;
            width: 100% !important;
            height: 3rem !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            margin-top: 1rem !important;
        }
        
        /* Progress Bar */
        .progress-container {
            width: 100%;
            height: 10px;
            background-color: #e2e8f0;
            border-radius: 5px;
            margin: 1rem 0;
            overflow: hidden;
        }
        
        /* Stats */
        .stats-container {
            display: flex;
            justify-content: space-around;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }
        
        .stat-item {
            background-color: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            text-align: center;
            min-width: 150px;
            margin: 0.5rem;
        }
        
        .stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #2b6cb0;
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: #2d3748;
        }
        
        /* Hide Streamlit elements we don't want */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Make file uploader more professional */
        .stFileUploader > div > div {
            padding: 2rem !important;
            border: 2px dashed #cbd5e0 !important;
            border-radius: 10px !important;
        }
        
        .stFileUploader > div > div:hover {
            border-color: #2b6cb0 !important;
        }
        
        /* Footer */
        .footer {
            text-align: center; 
            margin-top: 3rem; 
            padding-top: 2rem; 
            border-top: 1px solid #e9ecef; 
            color: #4a5568;
            font-size: 0.9rem;
        }
        
        /* Empty state */
        .empty-state {
            text-align: center; 
            padding: 4rem 2rem; 
            background-color: white; 
            border-radius: 15px; 
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        }
        
        .empty-state-title {
            margin-top: 2rem; 
            color: #2d3748;
        }
        
        .empty-state-text {
            color: #4a5568;
            max-width: 500px; 
            margin: 1rem auto;
        }
        
        /* Custom dropdown for Input Method Selection */
        .custom-select {
            width: 100%;
            margin-bottom: 1rem;
        }
        
        .select-option {
            display: inline-block;
            width: 48%;
            text-align: center;
            padding: 0.75rem 0;
            margin-right: 2%;
            background-color: #f0f4f8;
            color: #1a365d;
            border: 2px solid #90cdf4;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .select-option:last-child {
            margin-right: 0;
        }
        
        .select-option:hover {
            background-color: #ebf8ff;
            border-color: #2b6cb0;
        }
        
        .select-option.active {
            background-color: #2b6cb0;
            color: white;
            border-color: #2b6cb0;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-container">
        <div class="logo-text">🧠 AI Flashcard Generator</div>
        <div class="subtitle">Transform any text or image into intelligent study materials</div>
    </div>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = {}
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'cards_generated' not in st.session_state:
    st.session_state.cards_generated = 0
if 'texts_processed' not in st.session_state:
    st.session_state.texts_processed = 0
if 'last_shuffle_state' not in st.session_state:
    st.session_state.last_shuffle_state = False
if 'shuffled_keys' not in st.session_state:
    st.session_state.shuffled_keys = []
if 'input_method' not in st.session_state:
    st.session_state.input_method = "Text"

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Controls")
    
    # Stats display
    st.markdown("### 📊 Session Stats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="stat-item">
                <div class="stat-value">{st.session_state.cards_generated}</div>
                <div class="stat-label">Cards Generated</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-item">
                <div class="stat-value">{st.session_state.texts_processed}</div>
                <div class="stat-label">Texts Processed</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Options
    st.markdown("### 🔧 Options")
    shuffle_cards = st.checkbox("Shuffle Cards", value=False)
    
    # Help section
    st.markdown("### ❓ Help")
    with st.expander("How to use"):
        st.markdown("""
        1. Choose input method (Text or Image)
        2. Enter text or upload an image
        3. Generate flashcards
        4. Navigate through your cards
        5. Use text-to-speech for audio learning
        """)
    
    with st.expander("About"):
        st.markdown("""
        This AI-powered flashcard generator uses natural language processing 
        to create effective study materials from any text or image.
        
        It employs advanced algorithms to identify key concepts and 
        generate concise, memorable flashcards.
        """)

# Main content
col1, col2 = st.columns([1, 2])

with col1:
    # st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    # Custom title for input method
    st.markdown('<div class="input-method-title">Choose Your Input Method</div>', unsafe_allow_html=True)
    
    # Custom input method selector with better contrast instead of radio buttons
    col_text, col_image = st.columns(2)
    
    with col_text:
        text_active = "active" if st.session_state.input_method == "Text" else ""
        if st.button("Text", key="text_btn", use_container_width=True):
            st.session_state.input_method = "Text"
            st.rerun()
            
    with col_image:
        image_active = "active" if st.session_state.input_method == "Image" else ""
        if st.button("Image", key="image_btn", use_container_width=True):
            st.session_state.input_method = "Image"
            st.rerun()
    
    # Style the selected option
    st.markdown(f"""
        <script>
            document.querySelector('[data-testid="stButton"] button:contains("Text")').classList.add('select-option');
            document.querySelector('[data-testid="stButton"] button:contains("Text")').classList.add('{text_active}');
            document.querySelector('[data-testid="stButton"] button:contains("Image")').classList.add('select-option');
            document.querySelector('[data-testid="stButton"] button:contains("Image")').classList.add('{image_active}');
        </script>
    """, unsafe_allow_html=True)
    
    with st.form(key="input_form"):
        if st.session_state.input_method == "Text":
            text_input = st.text_area("Enter your text to generate flashcards:", height=300)
            submit_button = st.form_submit_button("Generate Flashcards", use_container_width=True)
            
            if submit_button:
                if text_input.strip():
                    with st.spinner("Generating intelligent flashcards..."):
                        flashcards = generate_flashcards(text_input)
                        st.session_state.flashcards = flashcards
                        st.session_state.current_index = 0
                        st.session_state.cards_generated += len(flashcards)
                        st.session_state.texts_processed += 1
                else:
                    st.warning("Please enter some text!")

        elif st.session_state.input_method == "Image":
            uploaded_file = st.file_uploader("Upload an image containing text", type=["png", "jpg", "jpeg"])
            submit_button = st.form_submit_button("Extract & Generate Flashcards", use_container_width=True)
            
            if submit_button:
                if uploaded_file is not None:
                    with st.spinner("Processing image and generating flashcards..."):
                        image_path = f"temp_{uploaded_file.name}"
                        with open(image_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        extracted_text = extract_text(image_path)
                        flashcards = generate_flashcards(extracted_text)
                        st.session_state.flashcards = flashcards
                        st.session_state.current_index = 0
                        st.session_state.cards_generated += len(flashcards)
                        st.session_state.texts_processed += 1
                else:
                    st.warning("Please upload an image!")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if st.session_state.flashcards and len(st.session_state.flashcards) > 0:
        flashcards = st.session_state.flashcards
        current_index = st.session_state.current_index
        
        # If shuffle is enabled and cards are loaded, shuffle them
        if shuffle_cards and st.session_state.last_shuffle_state != shuffle_cards:
            keys = list(flashcards.keys())
            random.shuffle(keys)
            st.session_state.shuffled_keys = keys
        
        st.session_state.last_shuffle_state = shuffle_cards
        
        # Use original or shuffled keys
        if shuffle_cards and len(st.session_state.shuffled_keys) > 0:
            keys = st.session_state.shuffled_keys
        else:
            keys = list(flashcards.keys())
            
        values = [flashcards[k] for k in keys]
        
        # Progress bar
        progress = (current_index + 1) / len(flashcards) if flashcards else 0
        st.markdown(f"""
            <div class="progress-container">
                <div style="height: 100%; width: {progress * 100}%; background-color: #2b6cb0;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        # Flashcard display
        st.markdown('<div class="flashcard-container">', unsafe_allow_html=True)
        
        # Make sure current_index is within bounds
        if current_index >= len(values):
            st.session_state.current_index = len(values) - 1
            current_index = st.session_state.current_index
            
        if current_index < 0:
            st.session_state.current_index = 0
            current_index = 0
            
        st.markdown(f"""
            <div class="flashcard">
                <div class="card-content">{values[current_index]}</div>
                <div class="card-counter">{current_index + 1}/{len(flashcards)}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation buttons
        col_left, col_middle, col_right = st.columns([1, 2, 1])
        
        with col_left:
            prev_disabled = current_index == 0
            if st.button("⬅️ Previous", key="prev_btn", disabled=prev_disabled):
                st.session_state.current_index -= 1
                st.rerun()
        
        with col_middle:
            if st.button("🔊 Read Aloud", key="audio_btn"):
                with st.spinner("Converting to speech..."):
                    text_to_speech(values[current_index])
                    st.success("Audio saved as 'flashcard.mp3'")
        
        with col_right:
            next_disabled = current_index == len(flashcards) - 1
            if st.button("Next ➡️", key="next_btn", disabled=next_disabled):
                st.session_state.current_index += 1
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display the key phrase (optional)
        with st.expander("Show Key Phrase"):
            st.write(f"**Key Phrase:** {keys[current_index]}")
    else:
        # Empty state
        st.markdown("""
            <div class="empty-state">
                <h2 class="empty-state-title">No Flashcards Yet</h2>
                <p class="empty-state-text">
                    Enter your study material or upload an image on the left to generate AI-powered flashcards.
                </p>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        Smart Flashcard Generator • Powered by AI  <br>
            © Chinmay Keripale & Asim Kazi 
    </div>
""", unsafe_allow_html=True)
