import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image, UnidentifiedImageError

# Optional integrations
try:
    import google.generativeai as genai
except:
    genai = None

try:
    from openai import OpenAI
except:
    OpenAI = None

try:
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import Chroma
except:
    OpenAIEmbeddings = None
    Chroma = None

# Local RAG engine
from rag_engine import (
    load_faqs,
    keyword_match,
    ensure_vectorstore,
    semantic_search
)

# Load .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# OpenAI Client
if OPENAI_API_KEY and OpenAI is not None:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
else:
    openai_client = None

# Gemini Client
if GEMINI_API_KEY and genai is not None:
    genai.configure(api_key=GEMINI_API_KEY)


# ---------------- STREAMLIT PAGE SETTINGS ----------------
st.set_page_config(page_title="Rooman Support Assistant", layout="wide")

# ------------------------ CSS STYLING ---------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #eaf2ff, #ffffff);
    font-family: 'Segoe UI', sans-serif;
}
.header {
    background: linear-gradient(90deg,#003A74,#005BB5);
    color: white;
    padding: 20px;
    font-size: 28px;
    border-radius: 10px;
    text-align: center;
    font-weight: 700;
}
.chat-box {
    background: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
}
.user-msg {
    background: #e6f0ff;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
    border-left: 4px solid #005BB5;
}
.bot-msg {
    background: #f3fff0;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
    border-left: 4px solid #2e7d32;
}
.sidebar-logo {
    text-align: center;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------- HEADER ----------------------------
st.markdown('<div class="header">Rooman Support Assistant</div>', unsafe_allow_html=True)


# -------------------------- SIDEBAR -------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
    try:
        img = Image.open("assets/rooman_logo.jpeg")
        st.image(img, use_container_width=True)   # Updated parameter
    except:
        st.warning("Logo missing or corrupted. Replace assets/rooman_logo.jpeg")

    st.markdown("### Menu")
    st.markdown("- Home\n- Chat Assistant\n- FAQ Manager")
    st.markdown("---")

    uploaded = st.file_uploader("Upload faqs.txt", type=["txt"])
    if uploaded:
        content = uploaded.getvalue().decode("utf-8")
        with open("data/faqs.txt", "w", encoding="utf-8") as f:
            f.write(content)
        st.success("FAQ updated! Click Rebuild Embeddings.")

    if st.button("🔁 Rebuild Embeddings"):
        ok = ensure_vectorstore("data/faqs.txt")
        if ok:
            st.success("Embeddings rebuilt successfully.")
        else:
            st.error("LangChain/Chroma not installed.")

    support_email = st.text_input("Support email", value="support@roomantech.com")
    st.markdown("---")
    st.caption("Rooman Technologies — AI Team")


# ------------------------ MAIN CHAT UI ---------------------
st.markdown('<div class="chat-box">', unsafe_allow_html=True)
st.subheader("How can I assist you today?")

if "history" not in st.session_state:
    st.session_state.history = []

FAQ_ITEMS = load_faqs("data/faqs.txt")

query = st.text_input("Type your question...")

# ---------- AI FUNCTIONS ----------
def call_openai(prompt):
    if openai_client is None:
        return None
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250
        )
        return response.choices[0].message.content.strip()
    except:
        return None

def call_gemini(prompt):
    if genai is None:
        return None
    try:
        model = genai.GenerativeModel("gemini-pro")
        resp = model.generate_content(prompt)
        return resp.text
    except:
        return None


# ------------------------ HANDLE CHAT ----------------------
if st.button("Send") and query:
    # 1) Keyword match
    matches = keyword_match(query, FAQ_ITEMS)
    
    if matches:
        best = matches[0][1]
        answer = f"### {best['q']}\n\n{best['a']}"
    else:
        # 2) Semantic RAG search
        docs = semantic_search(query, top_k=3)
        if docs:
            context = "\n---\n".join(docs)
            prompt = f"""
            CONTEXT:
            {context}

            QUESTION: {query}

            If unsure, escalate to {support_email}.
            """
            answer = call_openai(prompt) or call_gemini(prompt)
        else:
            # 3) Fallback plain LLM
            prompt = f"""
            User asked: {query}
            If you don't know the answer, say:
            'Please contact support at {support_email}'
            """
            answer = call_openai(prompt) or call_gemini(prompt)

    if not answer:
        answer = f"I'm not sure. Please contact support at {support_email}."

    st.session_state.history.append({"q": query, "a": answer})
    st.rerun()


# ------------------------ CHAT HISTORY ---------------------
for turn in reversed(st.session_state.history):
    st.markdown(f"<div class='user-msg'><b>You:</b> {turn['q']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='bot-msg'><b>Assistant:</b><br>{turn['a']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------- FAQ PREVIEW -----------------------
st.subheader("Frequently Asked Questions")
for item in FAQ_ITEMS[:10]:
    st.markdown(f"**{item['q']}**<br>{item['a']}<br><br>", unsafe_allow_html=True)
