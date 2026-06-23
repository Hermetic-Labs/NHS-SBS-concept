import json
import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import numpy as np
import markdown

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="NHS SBS CQ Portal Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount data folder for static media
app.mount("/data", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "data")), name="data")

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "cq_index.json")
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "markdown_docs")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "deepseek-coder-6.7b-instruct.Q4_K_M.gguf")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

cq_data = load_data()

# Global LLM instance
llm = None

def get_llm():
    global llm
    if llm is None and os.path.exists(MODEL_PATH):
        try:
            logger.info(f"Attempting to load local model from {MODEL_PATH}")
            from llama_cpp import Llama
            llm = Llama(model_path=MODEL_PATH, n_ctx=2048, verbose=True)
            logger.info("Model loaded successfully!")
        except ImportError:
            logger.error("llama-cpp-python is not installed. Waiting for build to finish.")
        except Exception as e:
            logger.error(f"Failed to load LLM: {e}")
    elif not os.path.exists(MODEL_PATH):
        logger.warning(f"Model path does not exist: {MODEL_PATH}")
    return llm

# ---------------------------------------------------------
# Semantic Retrieval System (TF-IDF Vectorization)
# ---------------------------------------------------------
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    logger.info("Building TF-IDF Semantic Vector Index...")
    corpus_docs = []
    
    # 1. Add CQs
    for row in cq_data:
        doc = " ".join([str(v) for v in row.values() if v])
        keys = list(row.keys())
        q = row.get(keys[1], str(row))
        a = row.get(keys[2], "Pending")
        corpus_docs.append({
            "text": doc,
            "type": "cq",
            "q": q,
            "a": a
        })
        
    # 2. Add Markdown Docs (Context-Aware)
    import re
    if os.path.exists(DOCS_DIR):
        for filename in os.listdir(DOCS_DIR):
            if not filename.endswith(".md") or "Bidder_Copy_Clarification" in filename:
                continue
            path = os.path.join(DOCS_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            doc_title = filename.replace('.md', '')
            current_header = doc_title
            current_chunk = []
            
            def save_chunk():
                if current_chunk:
                    text = " ".join(current_chunk).strip()
                    if len(text) > 20: # ignore noise
                        corpus_docs.append({
                            "text": f"{current_header}: {text}",
                            "type": "literature",
                            "source": current_header,
                            "content": text
                        })
                    current_chunk.clear()
            
            for line in lines:
                line = line.strip()
                if not line: continue
                if line.startswith("#"):
                    save_chunk()
                    current_header = f"{doc_title} > {line.lstrip('#').strip()}"
                else:
                    current_chunk.append(line)
                    if len(" ".join(current_chunk)) > 500: # chunk size boundary
                        save_chunk()
            save_chunk()

    corpus = [d["text"] for d in corpus_docs]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    logger.info(f"Semantic Vector Index Built Successfully with {len(corpus)} items.")
    
except ImportError:
    logger.warning("scikit-learn not installed yet. Waiting for background pip install to finish.")
    vectorizer = None
    tfidf_matrix = None
    corpus_docs = []

class ChatMessage(BaseModel):
    message: str

def semantic_search(query: str, top_k: int = 3):
    """Uses cosine similarity over TF-IDF vectors for true semantic retrieval."""
    if vectorizer is None or tfidf_matrix is None:
        return []
        
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    # Get top K indices
    top_indices = similarities.argsort()[-top_k:][::-1]
    
    results = []
    for idx in top_indices:
        if similarities[idx] > 0.05: # Minimum confidence threshold
            results.append(corpus_docs[idx])
            
    return results

@app.post("/api/chat")
def chat_inference(req: ChatMessage):
    """Core piping: Takes user message, finds context, and asks the model."""
    model = get_llm()
    if not model:
        logger.error("Inference request failed: Model offline.")
        def offline(): yield "[System Offline] Local LLM could not be loaded."
        return StreamingResponse(offline(), media_type="text/plain")
    
    # 1. Retrieve Context
    logger.info(f"Incoming chat request: '{req.message}'")
    context_rows = semantic_search(req.message, top_k=3)
    logger.info(f"Semantic Search found {len(context_rows)} relevant literature rows.")

    if not context_rows:
        logger.info("No context matched the query threshold. Returning hard guardrail response.")
        def guardrail(): yield "The provided literature does not contain information on this topic. Please try rephrasing your question or check the official documents directly."
        return StreamingResponse(guardrail(), media_type="text/plain")
        
    context_str = ""
    for i, r in enumerate(context_rows):
        if r["type"] == "cq":
            context_str += f"--- Q{i+1}: {r['q']}\n--- A{i+1}: {r['a']}\n\n"
        else:
            context_str += f"--- Source: {r['source']}\n--- Content: {r['content']}\n\n"

    # 2. Construct Prompt
    prompt = f"""You are an AI assistant built to help NHS suppliers understand the SBS10523 Healthcare AI framework.
You must synthesize an answer based ONLY on the provided context. Do not apologize. If the context does not contain the answer, say 'The provided literature does not contain information on this topic.'
CRITICAL INSTRUCTION: You must provide a complete, finished thought. Do not stop mid-sentence. Be concise.

LITERATURE CONTEXT:
{context_str}

USER: {req.message}
ASSISTANT:"""

    # 3. Model Inference (Streaming)
    def generate():
        response_stream = model(prompt, max_tokens=600, stop=["USER:", "\n\n\n", "ASSISTANT:"], temperature=0.15, repeat_penalty=1.15, stream=True)
        for chunk in response_stream:
            text = chunk['choices'][0]['text']
            if text:
                yield text

    return StreamingResponse(generate(), media_type="text/plain")

@app.get("/api/docs")
def list_docs():
    if not os.path.exists(DOCS_DIR):
        return {"docs": []}
    
    # Return pretty names and filenames
    files = [f for f in os.listdir(DOCS_DIR) if f.endswith('.md')]
    docs = [{"filename": f, "title": f.replace('.md', '').replace('_', ' ')} for f in files]
    return {"docs": docs}

@app.get("/api/docs/{doc_name}")
def get_doc(doc_name: str):
    path = os.path.join(DOCS_DIR, doc_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            md_content = f.read()
            html_content = markdown.markdown(md_content, extensions=['tables'])
            return {"html": html_content}
    raise HTTPException(status_code=404, detail="Document not found")

@app.get("/api/data")
def get_raw_data():
    """Serves the flattened CQ JSON directly."""
    return {"data": cq_data}

@app.get("/api/ping")
def ping():
    return {"status": "ok", "model_loaded": os.path.exists(MODEL_PATH)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7778)
