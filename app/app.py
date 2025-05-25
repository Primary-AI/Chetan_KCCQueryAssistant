import streamlit as st
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import subprocess
import os
import requests
from bs4 import BeautifulSoup
import time

# === CONFIGURATION ===
MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
FAISS_INDEX_PATH = "vector_store/faiss_index/index.faiss"
VECTOR_PATH = "vector_store/vectors.npy"
TEXTS_PATH = "vector_store/texts.json"
OLLAMA_PATH = "C:\\Users\\charu\\AppData\\Local\\Programs\\Ollama\\ollama.exe"  # Update as needed

# === STREAMLIT PAGE CONFIGURATION ===
st.set_page_config(
    page_title="KCC Query Assistant",
    layout="centered",
    page_icon="🌿",
    initial_sidebar_state="auto"
)

# === CUSTOM CSS STYLING ===
st.markdown("""
    <style>
    body {
        background-color: #394e3b;
        background-image: none;
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .main {
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0px 0px 20px rgba(0, 100, 0, 0.1);
        margin-top: 2rem;
    }
    .stTextInput>div>div>input {
        font-size: 1rem;
        background-color: rgba(200, 255, 200, 0.35);
        color: white;
    }
    .stButton>button {
        background-color: #388e3c;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #2e7d32;
        color: white;
    }
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# === LOAD COMPONENTS ===
@st.cache_resource
def load_model():
    return SentenceTransformer(MODEL_NAME)

@st.cache_resource
def load_faiss():
    return faiss.read_index(FAISS_INDEX_PATH)

@st.cache_data
def load_texts():
    with open(TEXTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_vectors():
    return np.load(VECTOR_PATH)

model = load_model()
index = load_faiss()
texts = load_texts()
vectors = load_vectors()

# === SEARCH FUNCTION ===
def search_query(query, top_k=5, threshold=0.5):
    query_vec = model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_vec, top_k)
    results = []
    for score, idx in zip(D[0], I[0]):
        if score < threshold:
            results.append((texts[idx], score))
    return results

# === OLLAMA CALL ===
def ask_ollama(question, context=None):
    if context:
        prompt = f"""
You are a Kisan Assistant AI trained to help Indian farmers.
Based on the following context, answer the user's query accurately:
---
{context}
---
User Question: {question}
"""
    else:
        prompt = f"""
You are a knowledgeable agricultural assistant AI. Provide the best possible answer based on your general understanding.
User Question: {question}
"""
    response = subprocess.run(
        [OLLAMA_PATH, "run", "llama3"],
        input=prompt,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return response.stdout.strip()

# === FALLBACK SEARCH ===
def fallback_duckduckgo(query):
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}+agriculture+india"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.find_all("a", class_="result__a")
        for link in links:
            href = link.get("href")
            text = link.text.lower()
            if any(word in text for word in ["crop", "soil", "farming", "irrigation", "india", "kisan", "agriculture"]):
                return href
        return None
    except:
        return None

# === UI LAYOUT ===
st.markdown("""<div class='main'>""", unsafe_allow_html=True)
st.markdown("## 🌿 KCC Query Assistant — Offline AI with FAISS + LLaMA3")
query = st.text_input("Enter your agricultural question:", placeholder="e.g. Fertilizer for Tomato in Tumkur?")
submit = st.button("Get Advice")

if query:
    with st.spinner("🧠 Thinking......"):
        def process():
            matches = search_query(query)
            if matches:
                context_block = "\n".join([m[0] for m in matches])
                st.markdown("### 🧠 Context Retrieved from Official KCC Dataset:")
                for m in matches:
                    question_part = query
                    answer_part = m[0].split('A:', 1)[-1].strip()
                    st.markdown(f"- **Q:** {question_part}\n\n  **A:** {answer_part}")
                answer = ask_ollama(query, context_block)
                st.success("✅ Answer generated using KCC dataset context")
                st.markdown(answer)
            else:
                st.warning("⚠️ No relevant context found in KCC database.")
                answer = ask_ollama(query)
                if answer:
                    st.info("💡 This answer is generated using general LLM knowledge (not from KCC dataset). Please verify before applying.")
                    st.markdown(answer)
                    result = fallback_duckduckgo(query)
                    if result:
                        st.markdown("### 🌐 Live Internet Search Result via DuckDuckGo:")
                        st.markdown(f"🔗 [Click here to view result]({result})")
                else:
                    st.error("❌ No answer was generated. Please try a more detailed or different question.")

        process()

st.markdown("""<hr><p style='text-align: center;'>✅ Built as part of the ANNAM.AI assignment.</p></div>""", unsafe_allow_html=True)
