# 🤖 Rooman Support Assistant — AI Powered Support Agent  
### Built with OpenAI + Gemini + LangChain + ChromaDB + Streamlit


Deployed on Streamlit :  https://roomansupportinpy-2dx2nejxdvkttsmerdxrkx.streamlit.app/

 
The **Rooman Support Assistant** is a fully functional AI-powered support chatbot that uses:

- 🔹 **Keyword-based FAQ matching**  
- 🔹 **AI-based semantic search (RAG)**  
- 🔹 **Multi-model fallback (OpenAI → Gemini)**  
- 🔹 **ChromaDB vector database**  
- 🔹 **LangChain embeddings**  
- 🔹 **Streamlit UI**  
- 🔹 **Rooman-styled branded interface**

It answers support questions automatically using FAQ documents + AI context understanding.

---

# 🚀 Features

### ✅ 1. Keyword Matching  
Fast rule-based matching using predefined FAQ keywords.

### ✅ 2. RAG (Retrieval Augmented Generation)  
If keywords fail, the system uses **semantic embeddings** + **ChromaDB** to find context.

### ✅ 3. Multi-Model AI Fallback  
Pipeline:

```
Keyword Match → RAG Search → OpenAI GPT-4o-mini → Gemini-Pro → Escalation
```

### ✅ 4. Upload New FAQs Anytime  
Through Streamlit sidebar.

### ✅ 5. Embeddings Rebuild Button  
Rebuild ChromaDB vector embeddings with single click.

### ✅ 6. Elegant Rooman UI  
- Sidebar with Rooman branding  
- Gradient headers  
- Chat bubbles  
- FAQ preview section  

### ✅ 7. Deployment-ready  
Works on **Streamlit Cloud**, **GitHub Codespaces**, **Local machine**, etc.

---

# 📁 Project Structure

```
rooman-support-assistant/
│
├── main.py
├── rag_engine.py
│
├── data/
│   └── faqs.txt
│
├── assets/
│   └── rooman_logo.jpeg
│
├── vectorstore/
│   └── chroma_db/            # auto-generated embeddings
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🧠 Architecture Overview

```
           ┌────────────────────────────┐
           │        User Input          │
           └──────────────┬────────────┘
                          │
        ┌─────────────────▼──────────────────┐
        │    Keyword Matching (Fast Lookup)   │
        └──────────────┬─────────────────────┘
                       │ No Match
                       ▼
        ┌──────────────────────────────────────┐
        │    RAG Engine (LangChain + Chroma)    │
        │ Semantic Vector Search on FAQs        │
        └──────────────┬───────────────────────┘
                       │ No Context
                       ▼
        ┌──────────────────────────────────────┐
        │  AI Generation (OpenAI GPT-4o-mini)   │
        └──────────────┬───────────────────────┘
                       │ Error / No Output
                       ▼
        ┌──────────────────────────────────────┐
        │       Gemini-Pro Fallback Model       │
        └──────────────┬───────────────────────┘
                       │
                       ▼
            Final Answer → UI Display
```

---

# ⚙️ Installation (Local)

### 1️⃣ Clone Repo
```
git clone https://github.com/YOUR_USERNAME/rooman-support-assistant.git
cd rooman-support-assistant
```

### 2️⃣ Create Virtual Environment
#### Windows:
```
python -m venv venv
venv\Scripts\activate
```

#### Mac / Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

### 4️⃣ Add API Keys  
Create `.env` file:

```
OPENAI_API_KEY=sk-xxxx
GEMINI_API_KEY=AIzaSyxxxx
```

**Do NOT upload `.env` to GitHub!**

### 5️⃣ Run App
```
streamlit run main.py
```

---

# ☁️ Deployment (Streamlit Cloud)

### 1. Push project to GitHub  
Make sure `.env` is NOT uploaded.

### 2. Go to Streamlit Cloud  
https://share.streamlit.io

### 3. Create New App  
- Repo → your GitHub repo  
- Branch → main  
- File → `main.py`

### 4. Add Secrets  
Go to **Settings → Secrets** and add:

```
OPENAI_API_KEY="sk-xxxx"
GEMINI_API_KEY="AIzaSyxxxx"
```

### 5. Deploy  
Your app will be live at something like:

```
https://yourname-rooman-support.streamlit.app
```

---

# 🧪 Testing the Chatbot

Try questions like:

- *"I want a refund" → matches refund FAQ*  
- *"Change my password" → matches password FAQ*  
- *"What are your working hours?"*  
- *"Contact support"*

If keyword fails → it uses vector search  
If vector fails → OpenAI  
If OpenAI fails → Gemini  
If all fail → escalates to support email  

---

# 🔒 Why Two AI APIs Used?

We use **OpenAI + Gemini** for:

### 1️⃣ Reliability  
If one model fails, the other replies.

### 2️⃣ Better accuracy  
OpenAI GPT-4o-mini is excellent for support answers.  
Gemini-Pro is excellent fallback and cheaper.

### 3️⃣ Safe enterprise architecture  
Multi-model fallback ensures **0% downtime**.

### 4️⃣ Rooman interview advantage  
This shows:
- Multi-model routing  
- Fault-tolerant design  
- Real-world AI agent architecture  

---

# 😎 Author

**Developed by:**  
Rooman Technologies — AI Assistant Project  
V Veeresh

---


