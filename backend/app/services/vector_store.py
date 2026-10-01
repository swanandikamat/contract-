import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any
from backend.app.core.config import settings
from backend.app.services.embedding_service import EmbeddingService

class VectorStore:
    """
    Manages persistent ChromaDB vector storage and semantic nearest-neighbor retrieval.
    """
    def __init__(self):
        settings.VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(settings.VECTOR_DB_DIR))
        self.collection = self.client.get_or_create_collection(
            name=settings.VECTOR_COLLECTION_NAME,
            metadata={"description": "Legal contract benchmark clauses collection"}
        )

    def count(self) -> int:
        return self.collection.count()

    def add_reference_clauses(self, reference_clauses: List[Dict[str, Any]]):
        """
        Indexes a list of reference clause objects into ChromaDB.
        Each item in reference_clauses must contain:
          - id: str
          - text: str
          - metadata: dict (e.g. filename, category_label: CLEAN/PROB, clause_id, header)
        """
        if not reference_clauses:
            return

        ids = [item["id"] for item in reference_clauses]
        texts = [item["text"] for item in reference_clauses]
        metadatas = [item["metadata"] for item in reference_clauses]

        embeddings = EmbeddingService.embed_batch(texts)

        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )
        print(f"[VectorStore] Indexed {len(ids)} reference clauses into ChromaDB collection '{settings.VECTOR_COLLECTION_NAME}'.")

    def search_similar(self, query_text: str, top_k: int = None) -> List[Dict[str, Any]]:
        """
        Performs semantic similarity search against indexed reference clauses.
        Returns a list of top-K matching reference clauses with distance/similarity scores.
        """
        k = top_k or settings.TOP_K_RESULTS
        if self.collection.count() == 0:
            return []

        query_embedding = EmbeddingService.embed_text(query_text)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(k, self.collection.count()),
            include=["documents", "metadatas", "distances"]
        )

        matches = []
        if results and results.get("documents"):
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            dists = results["distances"][0]

            for doc, meta, dist in zip(docs, metas, dists):
                # Convert L2 / Cosine distance to similarity score (0.0 to 1.0)
                similarity = max(0.0, min(1.0, 1.0 - (dist / 2.0)))
                matches.append({
                    "text": doc,
                    "metadata": meta,
                    "distance": dist,
                    "similarity_score": round(similarity, 4)
                })

        return matches
