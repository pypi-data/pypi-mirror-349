from langchain.schema import Document
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import LlamaCpp
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os # Import os for path handling

# Initialize these globally, but allow them to be reconfigured
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = None # Will be loaded dynamically
retriever = None   # Will be set dynamically
llm = None         # Will be initialized dynamically
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
qa_chain = None # Will be initialized dynamically

def set_llm_config(config):
    global llm, qa_chain, vectorstore, retriever
    
    # Ensure FAISS index is loaded before initializing LLM dependent components
    if not os.path.exists("faiss_index"):
        raise FileNotFoundError("FAISS index 'faiss_index' not found. Please run 'ragbot --local_docs_path <path> --serve' first.")
    
    # Load FAISS index if not already loaded
    if vectorstore is None:
        vectorstore = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever()

    llm = LlamaCpp(
        model_path=config.get("model_path"),
        n_ctx=config.get("n_ctx"),
        max_tokens=config.get("max_tokens"),
        n_threads=config.get("n_threads"),
        temperature=config.get("temperature"),
        verbose=False # Set to True for more verbose output from LlamaCpp
    )

    # Initialize conversation memory (stores chat history for session)
    # Re-initialize qa_chain with the new LLM
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        memory=memory,
        return_source_documents=True
    )
    # Tell memory key where to store answer
    qa_chain.memory.output_key = "answer"
    print("[RAGBOT] LLM and QA chain initialized with provided configuration.")


class FakeRetriever:
    def __init__(self, docs: list[Document]):
        self.docs = docs

    def get_relevant_documents(self, query: str):
        return self.docs

    def invoke(self, input, config=None):
        # input expected to be query string
        return self.get_relevant_documents(input)


def rerank_documents(query: str, docs: list[Document]) -> list[Document]:
    """
    Your reranking logic here.
    Return top 5 docs from top 10 after reranking.
    """
    # Dummy rerank (just top 5)
    return docs[:5]


def generate_answer(query: str) -> str:
    """
    Get relevant docs, rerank, then ask QA chain with updated retriever.
    """
    if llm is None or qa_chain is None or retriever is None:
        raise RuntimeError("LLM, QA Chain, or Retriever not initialized. Call set_llm_config first.")

    docs = retriever.get_relevant_documents(query)
    top_docs = rerank_documents(query, docs)

    # Inject reranked docs via FakeRetriever for this call
    original_retriever = qa_chain.retriever
    qa_chain.retriever = FakeRetriever(top_docs)

    # Pass query and chat_history to chain
    result = qa_chain({
        "question": query,
        "chat_history": qa_chain.memory.load_memory_variables({})["chat_history"]
    })

    # Restore original retriever after call
    qa_chain.retriever = original_retriever

    return result["answer"]


def smart_agent_run_chat(query: str) -> str:
    """
    Run generate_answer and filter bad/empty results.
    """
    local_answer = generate_answer(query)

    if local_answer and "i don't know" not in local_answer.lower() and len(local_answer.strip()) > 20:
        return local_answer

    # fallback or empty answer handling can go here
    return "Sorry, I couldn't find a good answer."


def multi_hop_rag(query: str) -> str:
    """
    1) Ask LLM to break query into simpler sub-questions
    2) Answer each sub-question updating chat history
    3) Ask final question with updated history
    """
    if llm is None or qa_chain is None or retriever is None:
        raise RuntimeError("LLM, QA Chain, or Retriever not initialized. Call set_llm_config first.")

    sub_question_prompt = f"""Break this complex question into two simpler questions:\nOriginal: "{query}"\n1."""
    sub_questions_text = llm.predict(sub_question_prompt)

    sub_questions = [
        line.strip().lstrip("1234567890. ").strip()
        for line in sub_questions_text.strip().split("\n")
        if line.strip()
    ]

    print("\n📌 Sub-questions generated:")
    for i, sq in enumerate(sub_questions, 1):
        print(f"  {i}. {sq}")

    for sq in sub_questions:
        print(f"\n🔁 Answering: {sq}")
        sub_ans = smart_agent_run_chat(sq)
        print(f"✅ Sub-answer: {sub_ans}")

    # Final answer with full chat history
    result = qa_chain({
        "question": query,
        "chat_history": qa_chain.memory.load_memory_variables({})["chat_history"]
    })

    return result["answer"]