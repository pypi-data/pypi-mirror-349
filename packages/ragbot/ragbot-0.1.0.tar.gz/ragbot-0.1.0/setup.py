import os
import subprocess
from setuptools import setup, find_packages

setup(
    name="ragbot",
    version="0.1.0",
    description="RAG chatbot for companies using local docs and websites",
    author="Preethi Chappidi",
    author_email="22b1074@iitb.ac.in",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain-community",             # Needed for specific loaders/tools
        "langchain-huggingface", 
        "faiss-cpu",
        "llama-cpp-python",
        "fastapi",
        "uvicorn",
        "beautifulsoup4",
        "requests",
        "sentence-transformers",
        "python-multipart",
        "tqdm",
        "nltk", # Added NLTK as it's used in document_loader.py
        "unstructured", # Added for PDF/Markdown loading
        "python-magic", # Dependency for unstructured
        "tiktoken", # Often a dependency for Langchain components
        #"pdfminer.six",                    # For PDF parsing
        #"pyOpenSSL",                       # If you do HTTPS or some web-related loaders
        #"pytesseract",                     # OCR - image to text
        #"onnxruntime>=1.18.0,<2.0.0",
        #"unstructured-inference",          # Used by `unstructured` for layout/model inference
        #"pi_heif",
        #"transformers==4.36.2",     # ✅ pinned for haystack
        #"pydantic<2.0.0",           # ✅ pinned for haystack  
        #"pdf2image"
    ],
    entry_points={
        "console_scripts": [
            "ragbot=ragbot.cli:main",
            "ragbot-download=ragbot.cli:download_model"
        ]
    },
    include_package_data=True,
    package_data={
        'ragbot': [
            'static/*',
            'static/chat.html',
            'static/chat_widget.html', # Make sure embed_ragbot.js is included
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)