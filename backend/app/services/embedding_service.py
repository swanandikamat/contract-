from typing import List, Union
from sentence_transformers import SentenceTransformer
from backend.app.core.config import settings

class EmbeddingService:
    """
    Generates dense vector embeddings using local sentence-transformers models.
    """
    _model = None

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        if cls._model is None:
            print(f"[EmbeddingService] Loading transformer model '{settings.EMBEDDING_MODEL_NAME}'...")
            cls._model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
            print("[EmbeddingService] Model loaded successfully.")
        return cls._model

    @classmethod
    def embed_text(cls, text: str) -> List[float]:
        """
        Embeds a single string into a 1D float vector.
        """
        model = cls.get_model()
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    @classmethod
    def embed_batch(cls, texts: List[str]) -> List[List[float]]:
        """
        Embeds a batch of strings into a list of 1D float vectors.
        """
        if not texts:
            return []
        model = cls.get_model()
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return embeddings.tolist()
