# 🌿 KCC Query Assistant — Offline AI with FAISS + LLaMA3

This project is a smart, offline-ready agricultural assistant designed to help farmers and agriculture officers get accurate crop-related answers using AI, even without an internet connection. It leverages semantic search using FAISS and sentence-transformers, and uses LLaMA3 via Ollama for LLM-based answer generation.

---

## ✅ Features

- 🔍 Top-k semantic search using FAISS + MPNet sentence embeddings
- 🧠 Contextual answer generation with LLaMA3 through Ollama
- 🧾 Retrieval from official KCC (Kisan Call Center) agricultural dataset
- 🌐 Internet fallback with DuckDuckGo for general LLM response + search
- 💡 Streamlit-based interactive user interface
- 🇮🇳 Localized for Indian farming needs

---

## 💻 Tech Stack

- `sentence-transformers/all-mpnet-base-v2`
- `FAISS` (CPU)
- `Ollama` with LLaMA3
- `Streamlit`
- `BeautifulSoup4` + `Requests` for fallback search

---

## 🚀 How to Run the Project

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Launch the Assistant

```bash
streamlit run app/app.py
```

> Make sure Ollama is running and LLaMA3 is downloaded locally.

---

## 📁 Project Structure

```
KCCQueryAssistant/
├── app/
│   └── app.py
├── code/
│   ├── 1_data_preprocessing.py
│   └── 2_generate_embeddings_and_faiss.py
├── data/
│   ├── cleaned_kcc.jsonl
├── vector_store/
│   ├── texts.json
├── requirements.txt
└── README.md
```

---

## 🧪 Working Logic

1. User enters a question related to agriculture.
2. The system searches top-k relevant KCC entries using FAISS.
3. If context is found:
   - LLaMA3 generates the answer using the retrieved context.
4. If context is not found:
   - A fallback DuckDuckGo internet search is triggered.
   - The LLM still attempts a general response.

---

## 🌾 Dataset Usage

- Official **KCC dataset of Karnataka** used.
- Original dataset size: **1.6 million entries**.
- Processed a representative **sample of 100,000 Q&A pairs** for embedding.

---

## 🌾 Sample Use Case

**Input:**  
`Fertilizer for Tomato in Tumkur?`

**→**  
- Context retrieved from KCC dataset  
- Answer generated using LLaMA3  
- Fallback search shown if no local match exists

---

## 📌 Notes

- LLaMA3 model must be available in Ollama locally
- Large files like `.faiss`, `.npy`, and `.csv` are excluded from the repo due to GitHub’s 100MB limit
- The app is optimized for regional agricultural queries in India
- Can be extended with multilingual support and voice integration

---

## 📄 License

This submission is part of the ANNAM.AI academic assignment.  
All data is used for educational purposes only.

---
✅ Developed for empowering Indian agriculture through AI
