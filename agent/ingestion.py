# agent/ingestion.py
import fitz  # pymupdf
from unstructured.partition.auto import partition
from bs4 import BeautifulSoup
import json
from agent.rag_engine import RAGEngine

def ingest_documents(files, html_file):
    """
    Read all support documents + checkout.html, convert them to plain text,
    and build the RAG knowledge base.
    """
    docs_content_parts = []

    # Process documents
    for f in files:
        filename = (f.filename or "").lower()

        try:
            if filename.endswith(".pdf"):
                file_bytes = f.read()
                with fitz.open(stream=file_bytes, filetype="pdf") as pdf:
                    for page in pdf:
                        docs_content_parts.append(page.get_text())

            elif filename.endswith(".json"):
                raw = f.read().decode("utf-8", errors="ignore")
                try:
                    obj = json.loads(raw)
                    docs_content_parts.append(json.dumps(obj, indent=2))
                except json.JSONDecodeError:
                    docs_content_parts.append(raw)

            elif filename.endswith(".md") or filename.endswith(".txt"):
                docs_content_parts.append(f.read().decode("utf-8", errors="ignore"))

            else:
                elements = partition(file=f)
                docs_content_parts.append(" ".join(
                    el.text for el in elements if hasattr(el, "text") and el.text
                ))

        finally:
            try:
                f.stream.seek(0)
            except Exception:
                pass

    # Process checkout.html
    html_bytes = html_file.read()
    soup = BeautifulSoup(html_bytes, "html.parser")

    html_text = soup.get_text(separator=" ", strip=True)
    html_pretty = soup.prettify()

    full_corpus = "\n".join(docs_content_parts) + "\n" + html_text

    rag = RAGEngine()
    rag.build_knowledge_base(full_corpus)

    # 🚀 Store full HTML separately to retrieve correctly in script_agent
    rag.collection.add(
        documents=[html_pretty],
        embeddings=[rag.model.encode(html_pretty)],
        ids=["checkout_html_full"]
    )

    return rag
