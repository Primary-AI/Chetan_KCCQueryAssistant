import pandas as pd
import json
import os

input_path = "data/StateName_KARNATAKA_dataset.csv"
output_path = "data/cleaned_kcc.jsonl"

print("🔍 Starting data preprocessing...")

# Load CSV
try:
    df = pd.read_csv(input_path, low_memory=False)
    print("✅ CSV loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load CSV: {e}")
    exit()

# Rename based on actual columns
df = df.rename(columns={
    "QueryText": "question",
    "KccAns": "answer",
    "Crop": "crop",
    "DistrictName": "district",
    "QueryType": "query_type",
    "Season": "season",
    "StateName": "state"
})

# Select only relevant columns
df = df[["question", "answer", "crop", "district", "query_type", "season", "state"]]

# Drop rows with missing Q&A
df = df.dropna(subset=["question", "answer"])
print(f"✅ Rows after dropping empty Q&A: {len(df)}")

# Sample 100K rows for fast embedding
df = df.sample(n=100000, random_state=42)

# Save cleaned data to JSONL
os.makedirs("data", exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    for record in df.to_dict(orient="records"):
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"✅ Cleaned {len(df)} Q&A pairs written to {output_path}")
