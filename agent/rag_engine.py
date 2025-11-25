from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb


class RAGEngine:
    def __init__(self):
        self.client = chromadb.Client()

        # Make sure we don't recreate existing collection
        try:
            self.collection = self.client.create_collection("knowledge_base")
        except:
            # If already exists, get it instead
            self.collection = self.client.get_collection("knowledge_base")

        # ✅ Correct indentation and CPU enforcement
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")

    def build_knowledge_base(self, text):
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(text)
        embeddings = self.model.encode(chunks)

        for i, chunk in enumerate(chunks):
            self.collection.add(
                documents=[chunk],
                embeddings=[embeddings[i]],
                ids=[str(i)]
            )

    def retrieve(self, query, k=5):
        q_emb = self.model.encode([query])[0]
        results = self.collection.query(query_embeddings=[q_emb], n_results=k)
        return results
