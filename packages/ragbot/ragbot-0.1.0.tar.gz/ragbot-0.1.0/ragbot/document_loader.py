import os
from bs4 import BeautifulSoup
import requests
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, UnstructuredPDFLoader, UnstructuredMarkdownLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from urllib.parse import urljoin, urlparse
from collections import deque
import time

def is_internal_link(base_url, link):
    parsed_base = urlparse(base_url)
    parsed_link = urlparse(urljoin(base_url, link))
    return parsed_base.netloc == parsed_link.netloc

def get_all_internal_links(base_url, max_pages=50):
    visited = set()
    to_visit = deque([base_url])
    found_links = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.popleft()
        if url in visited:
            continue
        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                continue
            visited.add(url)
            found_links.append(url)

            soup = BeautifulSoup(response.text, "html.parser")
            for a_tag in soup.find_all("a", href=True):
                link = urljoin(url, a_tag["href"])
                if is_internal_link(base_url, link) and link not in visited:
                    to_visit.append(link)

            time.sleep(0.5)  # be polite
        except Exception as e:
            print(f"[WARN] Error visiting {url}: {e}")

    return found_links


def sentence_chunker(docs, chunk_size=3, overlap=1):
    chunked_docs = []

    for doc in docs:
        sentences = sent_tokenize(doc.page_content)
        i = 0
        while i < len(sentences):
            chunk = sentences[i:i + chunk_size]
            if chunk:
                joined = " ".join(chunk)
                chunked_docs.append(Document(page_content=joined, metadata=doc.metadata))
            i += chunk_size - overlap  # slide with overlap

    return chunked_docs

def char_chunker(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.split_documents(docs)

def read_web_urls(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip() and line.startswith("http")]

def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        return text
    except Exception as e:
        print(f"[WARN] Failed to scrape {url}: {e}")
        return ""

def load_all_docs(folder_path, chunking="sentence"):
    raw_docs = []

    for fname in os.listdir(folder_path):
        path = os.path.join(folder_path, fname)

        # Website data
        if fname == "web_data.txt":
            urls = read_web_urls(path)
            for url in urls:
                all_links = get_all_internal_links(url)
                print(f"[INFO] Found {len(all_links)} pages under {url}")
                for link in all_links:
                    web_text = scrape_website(link)
                    if web_text:
                        raw_docs.append(Document(page_content=web_text, metadata={"source": link}))
            continue


        # Local file loading
        if fname.endswith(".pdf"):
            loader = UnstructuredPDFLoader(path)
        elif fname.endswith(".md"):
            loader = UnstructuredMarkdownLoader(path)
        else:
            loader = TextLoader(path)

        raw_docs.extend(loader.load())

    # Chunking
    if chunking == "char":
        return char_chunker(raw_docs)
    return sentence_chunker(raw_docs)

def embed_and_store(chunks, persist_path="faiss_index"):
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    vectorstore.save_local(persist_path)
    print(f"[INFO] FAISS index saved to {persist_path}")
