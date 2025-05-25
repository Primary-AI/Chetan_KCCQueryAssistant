from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os
from tqdm import tqdm

# === Step 1: Load cleaned data ===
print("🔍 Loading cleaned JSONL data...")
data_path = "data/cleaned_kcc.jsonl"
texts = []

with open(data_path, "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        q = item.get("question", "").strip()
        a = item.get("answer", "").strip()
        texts.append(f"Q: {q} A: {a}")

# === Step 2: Load best-in-class embedding model ===
print("🧠 Loading model: all-mpnet-base-v2...")
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# === Step 3: Generate embeddings in batches ===
print(f"⚙️ Generating embeddings for {len(texts)} entries in batches...")
batch_size = 500
all_embeddings = []

for i in tqdm(range(0, len(texts), batch_size), desc="Encoding batches"):
    batch = texts[i:i+batch_size]
    emb = model.encode(batch, convert_to_numpy=True)
    all_embeddings.append(emb)

embeddings = np.vstack(all_embeddings)

# === Step 4: Save raw data ===
os.makedirs("vector_store/faiss_index", exist_ok=True)
np.save("vector_store/vectors.npy", embeddings)
with open("vector_store/texts.json", "w", encoding="utf-8") as f:
    json.dump(texts, f, ensure_ascii=False)

# === Step 5: Build FAISS index ===
print("🧱 Building FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# === Step 6: Save the FAISS index ===
faiss.write_index(index, "vector_store/faiss_index/index.faiss")
print("✅ Embeddings + FAISS index saved successfully!")
