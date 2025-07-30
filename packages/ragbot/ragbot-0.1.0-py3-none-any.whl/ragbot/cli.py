import argparse
import os
import subprocess
import uvicorn
from ragbot.document_loader import load_all_docs, embed_and_store
from ragbot.ragbot_api import app  # import FastAPI app
from ragbot.ret import set_llm_config # Import the new setter function

def download_model():
    model_dir = "models"
    model_file = "llama-2-7b-chat.Q4_K_M.gguf"
    model_path = os.path.join(model_dir, model_file)

    if not os.path.exists(model_path):
        print("[CLI] Downloading LLaMA 2 model...")
        os.makedirs(model_dir, exist_ok=True)
        url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
        # Using curl instead of wget for broader compatibility, and ensures directory exists
        subprocess.run(["curl", "-L", url, "-o", model_path], check=True)
        print("[CLI] Model downloaded.")
    else:
        print("[CLI] Model already exists, skipping download.")


def main():
    parser = argparse.ArgumentParser(description="RAGBot CLI")
    parser.add_argument("--local_docs_path", required=True, help="Path to folder with local documents")
    parser.add_argument("--chunking", choices=["sentence", "char"], default="sentence", help="Chunking strategy")
    parser.add_argument("--serve", action="store_true", help="Start the API server after building index")
    
    # Add LLM configuration arguments
    parser.add_argument("--model_path", default="models/llama-2-7b-chat.Q4_K_M.gguf", help="Path to the LlamaCpp model file")
    parser.add_argument("--n_ctx", type=int, default=4096, help="Context window size for LLM")
    parser.add_argument("--max_tokens", type=int, default=512, help="Max tokens to generate by LLM")
    parser.add_argument("--n_threads", type=int, default=6, help="Number of threads for LLM")
    parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature for LLM")

    args = parser.parse_args()

    # Ensure model is downloaded if it's not already there
    download_model()

    print(f"[RAGBOT] Loading and chunking documents from: {args.local_docs_path}")
    documents = load_all_docs(args.local_docs_path, args.chunking)

    print(f"[RAGBOT] Total chunks created: {len(documents)}")
    print(f"[RAGBOT] Building FAISS index and saving...")

    embed_and_store(documents)
    print("[RAGBOT] Embedding and FAISS index creation done.")

    if args.serve:
        # Pass LLM configuration to the ret.py module
        llm_config = {
            "model_path": args.model_path,
            "n_ctx": args.n_ctx,
            "max_tokens": args.max_tokens,
            "n_threads": args.n_threads,
            "temperature": args.temperature,
        }
        set_llm_config(llm_config) # Call the new setter function

        print("[RAGBOT] Starting API server at http://localhost:8000")
        uvicorn.run(app, host="0.0.0.0", port=8000)