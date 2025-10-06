from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import torch
from groq import Groq
import os

# ===== Config =====
DATA_DIR = Path("data")
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ===== Groq API Key =====
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Please set GROQ_API_KEY as environment variable.")
client = Groq(api_key=GROQ_API_KEY)

# ===== Load docs and embeddings once =====
def load_documents():
    docs = []
    for file in DATA_DIR.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            docs.append(f.read().strip())
    return docs

app = Flask(__name__)
documents = load_documents()
model = SentenceTransformer(MODEL_NAME, device=DEVICE)
embeddings = model.encode(documents, convert_to_tensor=True)

# ===== Retrieval =====
def get_relevant_docs(query):
    query_emb = model.encode(query, convert_to_tensor=True)
    sims = util.pytorch_cos_sim(query_emb, embeddings)[0]
    top_k = torch.topk(sims, k=TOP_K)
    return [documents[i] for i in top_k.indices]

# ===== LLM =====
def generate_answer(question, context_list):
    context = "\n\n".join(context_list)
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile"
    )
    return response.choices[0].message.content.strip()

# ===== Routes =====
@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "").strip()
    if not question:
        return jsonify({"error": "Please ask a question"}), 400
    
    rel = get_relevant_docs(question)
    answer = generate_answer(question, rel)
    return jsonify({"answer": answer})

@app.route("/")
def serve_page():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
