import streamlit as st
import spacy

# ---------------------------------------------------------
# Prerequisites:
# 1. Install necessary libraries:
#    pip install streamlit spacy
# 2. Download the Russian language model for spaCy:
#    python -m spacy download ru_core_news_sm
# ---------------------------------------------------------

# Page configuration
st.set_page_config(page_title="Считай глаголы", page_icon="🍎")

# --- Custom CSS for Classic Mac OS System 1 Aesthetic ---
# We use st.markdown with unsafe_allow_html to inject CSS to style Streamlit elements.
# This emulates the low-resolution, monochrome, pixelated, blocky UI of System 1.
st.markdown("""
<style>
/* Global app styles */
.stApp {
    background-color: #f0f0f0; /* Slight off-white background */
    color: black;
    font-family: 'Courier New', Courier, monospace; /* Use monospace font */
}

/* Main title styling */
h1 {
    text-align: center;
    text-transform: uppercase;
    color: black;
    font-size: 2.2em;
    padding-bottom: 15px;
    border-bottom: 4px solid black;
    margin-bottom: 30px;
}

/* Text Area Input styling */
textarea {
    border: 3px solid black !important;
    background-color: white !important;
    color: black !important;
    font-family: 'Courier New', Courier, monospace !important;
    font-size: 1.1em !important;
    border-radius: 0px !important; /* Sharp corners */
    padding: 10px !important;
}

/* Button Styling (simple, rectangular, black/white) */
.stButton>button {
    background-color: white;
    color: black;
    border: 3px solid black !important;
    font-family: 'Courier New', Courier, monospace !important;
    font-weight: bold !important;
    font-size: 1.1em !important;
    text-transform: uppercase;
    border-radius: 0px !important; /* Sharp corners */
    width: 100%;
    padding: 10px !important;
    transition: background-color 0.1s ease-in-out;
}

.stButton>button:hover {
    background-color: black;
    color: white;
}

/* Metric Display Styling (The big verb count number) */
div[data-testid="stMetricValue"] {
    font-size: 5em !important;
    font-family: 'Courier New', Courier, monospace !important;
    font-weight: bold !important;
    color: black !important;
    text-align: center;
    border: 3px solid black;
    padding: 10px;
    background-color: white;
}

div[data-testid="stMetricLabel"] {
    font-size: 1.3em !important;
    font-family: 'Courier New', Courier, monospace !important;
    text-align: center;
    text-transform: uppercase;
    color: black !important;
    margin-top: 10px;
}

/* Style for warnings and error messages */
.stAlert {
    border: 3px solid black !important;
    border-radius: 0px !important;
    background-color: white !important;
    color: black !important;
}

/* Make the overall container look more like an old window */
.block-container {
    border: 5px solid black;
    padding: 2rem;
    margin-top: 2rem;
    background-color: #f8f8f8;
}

</style>
""", unsafe_allow_html=True)

# --- NLP Setup (spaCy for Russian) ---

# Load the Russian model. Cache it to avoid reloading on every interaction.
@st.cache_resource
def load_spacy_model():
    try:
        # Load the small Russian model. You can use 'ru_core_news_md' for slightly better accuracy.
        nlp = spacy.load("ru_core_news_sm")
        return nlp
    except OSError:
        st.error("⚠️ Russian spaCy model 'ru_core_news_sm' not found. "
                 "Please install it: `python -m spacy download ru_core_news_sm` "
                 "and restart the app.")
        return None

# Attempt to load the model
nlp_ru = load_spacy_model()

# Define the verb counting function
def count_verbs(text, nlp):
    if nlp is None or not text.strip():
        return 0
    # Process the text using spaCy
    doc = nlp(text)
    # Iterate through tokens and count those marked as VERB (Part of Speech)
    verb_count = sum(1 for token in doc if token.pos_ == "VERB")
    return verb_count

# --- App UI and Logic ---

# Title (Styled by CSS above)
st.title("Verb Counter / RU 🇷🇺")

# Text Area Input
text_input = st.text_area(
    "Введите текст на русском языке (Enter Russian text):",
    height=250,
    placeholder="Напишите или вставьте ваш текст здесь...",
    key="russian_text_input"
)

# Button to trigger the counting (Styled by CSS above)
if st.button("Count Verbs / Считать"):
    if not text_input.strip():
        st.warning("Ради бога, введите текст для анализа. (Please enter text to analyze.)")
    elif nlp_ru:
        # Perform the verb count
        num_verbs = count_verbs(text_input, nlp_ru)
        
        # Display the result using st.metric, which is styled into a large, simple box.
        st.metric(label="Глаголов", value=num_verbs)
        
        # Optional: Show a few examples of found verbs
        # doc = nlp_ru(text_input)
        # verbs_list = [token.text for token in doc if token.pos_ == "VERB"]
        # if verbs_list:
        #     st.write("**Найденные глаголы (Examples):**")
        #     st.write(", ".join(verbs_list[:15]) + ("..." if len(verbs_list) > 15 else ""))

# Footer / Instructions (Centered and styled subtly)
st.markdown("""
<div style="text-align: center; font-size: 0.8em; color: gray; margin-top: 30px;">
  ---<br>
  Classic Mac OS System 1 Interface styled Verb Counter.<br>
  Uses Streamlit & spaCy ('ru_core_news_sm').
</div>
""", unsafe_allow_html=True)
