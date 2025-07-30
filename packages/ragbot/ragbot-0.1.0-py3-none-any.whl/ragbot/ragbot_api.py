# ragbot/ragbot_api.py
import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from ragbot.ret import multi_hop_rag, set_llm_config # Import the new setter function

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.on_event("startup")
async def startup_event():
    # This event fires when the FastAPI application starts.
    # We will use the llm_config stored in app.state by cli.py
    # to initialize the LLM and QA chain in ret.py
    if hasattr(app.state, "llm_config"):
        set_llm_config(app.state.llm_config)
    else:
        # Fallback if app.state.llm_config is not set (e.g., direct uvicorn run for testing)
        # In a typical CLI flow, this branch won't be hit if --serve is used.
        # You might want to handle this more robustly, e.g., by logging a warning
        # or raising an error if the model path is critical and not set.
        print("[WARN] LLM configuration not set via CLI. Using default LlamaCpp params if not configured.")
        # If you want to force default initialization without CLI config, you could do:
        # set_llm_config({
        #     "model_path": "models/llama-2-7b-chat.Q4_K_M.gguf",
        #     "n_ctx": 4096, "max_tokens": 512, "n_threads": 6, "temperature": 0.7
        # })


@app.get("/chat.html")
def chat_page():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static/chat.html"))

@app.get("/chat_window.html")
def chat_window_page():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static/chat_window.html"))

@app.get("/")
def root_redirect():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static/chat.html"))


@app.post("/chat/")
async def chat_endpoint(request: QueryRequest):
    query = request.query
    answer = multi_hop_rag(query)
    return {"answer": answer}

# Mount the static directory
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")