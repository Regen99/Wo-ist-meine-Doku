from fastembed import TextEmbedding
import logging

class DiscoveryEmbedder:
    """
    Turbo-Lite Multilingual Embedder (MiniLM-L12-v2).
    Uses FastEmbed (ONNX) to remove the heavy PyTorch dependency.
    Extremely fast on CPU with a minimal memory footprint.
    384-dimensional output, 50+ languages supported.
    """

    # paraphrase-multilingual-MiniLM-L12-v2 is officially supported by FastEmbed
    # and shares the same 384-dim space as e5-small.
    MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    def __init__(self, use_gpu: bool = False):
        # fastembed handles device selection automatically
        # For our Lite version, it will default to optimized CPU inference
        logging.info(f"Initializing Turbo-Lite Embedder ({self.MODEL_NAME})...")
        
        try:
            self.model = TextEmbedding(model_name=self.MODEL_NAME)
        except Exception as e:
            logging.error(f"Failed to load FastEmbed model: {e}")
            raise

    def embed(self, text: list[str], task: str = "") -> list[list[float]]:
        """
        Generates 384-dimensional embeddings using FastEmbed.
        Input text should ideally be prefixed with 'query: ' or 'passage: '.
        Returns a list of lists of floats.
        """
        if not text:
            return []
            
        # FastEmbed's .embed() is a generator - we convert to list
        # It's highly optimized for batch processing
        embeddings_generator = self.model.embed(text)
        return [list(emb) for emb in embeddings_generator]

    def get_dim(self) -> int:
        return 384
