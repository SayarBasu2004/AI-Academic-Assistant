import streamlit as st
from llm import ask_llm
from prompts import (
    answer_question, summarize_text, explain_concept, 
    ask_from_document, generate_key_points, generate_questions
)
from PyPDF2 import PdfReader

# -------------------------------
# Page Config & Deep Dark Theme
# -------------------------------
st.set_page_config(page_title="Academic AI", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    .block-container { padding-top: 2rem; max-width: 850px; }
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
    }
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    h1, h2, h3 { color: #60a5fa !important; }
    </style>
    """, unsafe_allow_html=True)

# -------------------------------
# Session State Initialization
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_response" not in st.session_state:
    st.session_state.last_response = None
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.title("AI Modules")
    option = st.selectbox(
        "Choose Functionality",
        [
            "Answer Academic Question",
            "Summarize Text",
            "Explain Concept",
            "Ask from Document",
            "Generate Key Points / Notes",
            "Generate Questions from Text",
            "Upload PDF & Work With It"
        ]
    )
    st.divider()
    if st.button("Clear History"):
        st.session_state.chat_history = []
        st.session_state.last_response = None
        st.session_state.pdf_text = None
        st.rerun()

# -------------------------------
# 1. INPUT PANEL
# -------------------------------
st.title("Academic Assistant")

prompt = None
user_query = ""

with st.container(border=True):
    if option == "Answer Academic Question":
        user_query = st.text_area("Enter your academic question")
        if user_query.strip(): prompt = answer_question(user_query)

    elif option == "Summarize Text":
        user_query = st.text_area("Paste academic text")
        if user_query.strip(): prompt = summarize_text(user_query)

    elif option == "Explain Concept":
        concept = st.text_input("Enter concept")
        level = st.select_slider("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
        if concept.strip():
            user_query = f"Explain {concept} ({level})"
            prompt = explain_concept(concept, level)

    elif option == "Ask from Document":
        doc = st.text_area("Paste document text", height=150)
        q = st.text_input("Enter your question")
        if doc.strip() and q.strip():
            user_query, prompt = q, ask_from_document(doc, q)

    elif option == "Generate Key Points / Notes":
        user_query = st.text_area("Paste text for notes")
        if user_query.strip(): prompt = generate_key_points(user_query)

    elif option == "Generate Questions from Text":
        user_query = st.text_area("Paste text to generate quiz")
        if user_query.strip(): prompt = generate_questions(user_query)

    elif option == "Upload PDF & Work With It":
        uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
        if uploaded_pdf:
            st.session_state.pdf_text = extract_text_from_pdf(uploaded_pdf)
            st.success("PDF Processed")
            
            pdf_option = st.selectbox("Action", ["Summarize PDF", "Ask Question", "Key Points", "Generate Questions"])
            if pdf_option == "Summarize PDF":
                user_query, prompt = "Summarize PDF", summarize_text(st.session_state.pdf_text)
            elif pdf_option == "Ask Question":
                q = st.text_input("Question for PDF")
                if q: user_query, prompt = q, ask_from_document(st.session_state.pdf_text, q)
            elif pdf_option == "Key Points":
                user_query, prompt = "PDF Key Points", generate_key_points(st.session_state.pdf_text)
            elif pdf_option == "Generate Questions":
                user_query, prompt = "PDF Quiz", generate_questions(st.session_state.pdf_text)

    if st.button("GENERATE"):
        if prompt:
            with st.spinner("Processing..."):
                response = ask_llm(prompt)
                st.session_state.last_response = response
                # Store interaction
                st.session_state.chat_history.append({
                    "query": user_query, 
                    "response": response,
                    "relevance": 3, "clarity": 3, "completeness": 3
                })
        else:
            st.warning("Please provide valid input.")

# -------------------------------
# 2. OUTPUT & FEEDBACK
# -------------------------------
if st.session_state.last_response:
    st.markdown("Result")
    with st.container(border=True):
        st.markdown(st.session_state.last_response)
        
    with st.expander("Rate this response"):
        # We tie these to the latest item in chat_history
        idx = -1
        r = st.slider("Relevance", 1, 5, st.session_state.chat_history[idx]["relevance"], key="rel_slider")
        cl = st.slider("Clarity", 1, 5, st.session_state.chat_history[idx]["clarity"], key="cl_slider")
        co = st.slider("Completeness", 1, 5, st.session_state.chat_history[idx]["completeness"], key="co_slider")
        
        if st.button("Submit Feedback"):
            st.session_state.chat_history[idx]["relevance"] = r
            st.session_state.chat_history[idx]["clarity"] = cl
            st.session_state.chat_history[idx]["completeness"] = co
            st.success("Evaluation recorded!")

# -------------------------------
# 3. SESSION HISTORY
# -------------------------------
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("Session History")
    # Show ALL history in reverse order
    for chat in reversed(st.session_state.chat_history):
        with st.expander(f"📌 {chat['query'][:60]}..."):
            st.markdown(chat['response'])
            st.caption(f"Score: R:{chat['relevance']} | C:{chat['clarity']} | Comp:{chat['completeness']}")