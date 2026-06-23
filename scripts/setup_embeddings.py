import urllib.request
import os

MODEL_URL = "https://huggingface.co/CompendiumLabs/bge-small-en-v1.5-gguf/resolve/main/bge-small-en-v1.5-q4_k_m.gguf"
DEST_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "bge-small-en-v1.5-q4_k_m.gguf")

def download_model():
    print(f"Downloading Semantic Embedding Model (22MB) to {DEST_PATH}...")
    if not os.path.exists(DEST_PATH):
        urllib.request.urlretrieve(MODEL_URL, DEST_PATH)
        print("Download complete!")
    else:
        print("Model already exists.")

if __name__ == "__main__":
    download_model()
