from typing import Dict, List, Optional, Union
from sentence_transformers import SentenceTransformer
import uuid
import os
from urllib.parse import urlparse
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
import logging


logging.basicConfig(level=logging.DEBUG)


class VectorDB:
    def __init__(
        self,
        collection_name: str = "documents",
        model_name: str = "all-MiniLM-L6-v2",
        qdrant_url: Optional[str] = None,
        qdrant_api_key: Optional[str] = None,
        qdrant_path: Optional[str] = None,
        qdrant_port: Optional[int] = None,
    ):
        """Initialize the vector database connection with Qdrant

        Args:
            collection_name: Name for the Qdrant collection
            model_name: Name of the sentence-transformer model to use
            qdrant_url: URL for Qdrant cloud (if using cloud)
            qdrant_api_key: API key for Qdrant cloud (if using cloud)
            qdrant_path: Path for local Qdrant database (if using local)
            qdrant_port: Custom port for Qdrant server (overrides default 443/80)
        """
        self.collection_name = collection_name
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        # Connect to Qdrant (cloud or local)
        if qdrant_url and qdrant_api_key:
            # parse URL and default ports
            parsed = urlparse(qdrant_url)
            scheme = parsed.scheme or "http"
            host = parsed.hostname
            # use provided port or fall back to parsed port or standard HTTP/HTTPS
            port = qdrant_port or parsed.port or (443 if scheme == "https" else 80)
            # build full URL including port
            full_url = f"{scheme}://{host}:{port}"
            self.client = QdrantClient(
                url=full_url,
                api_key=qdrant_api_key,
                prefer_grpc=False
            )
        else:
            # Use in-memory or local path
            self.client = QdrantClient(path=qdrant_path)
        
        # Check if collection exists, create if not
        collections = self.client.get_collections().collections
        collection_names = [collection.name for collection in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.dimension, distance=Distance.COSINE),
            )
    
    def chunk_text(self, text: str, chunk_size: int = 200, overlap: int = 50) -> List[str]:
        """Split text into chunks with overlap
        
        Args:
            text: The text to chunk
            chunk_size: Size of each chunk in words
            overlap: Number of overlapping words between chunks
        
        Returns:
            List of text chunks
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
            if i + chunk_size >= len(words):
                break
                
        return chunks
    
    def add_documents(self, documents: Dict[str, str], chunk_size: int = 200, overlap: int = 50):
        """Parse, chunk, and add documents to the vector database
        
        Args:
            documents: Dictionary mapping document names to their text content
            chunk_size: Size of each chunk in words
            overlap: Number of overlapping words between chunks
        """
        points = []
        
        for name, text in documents.items():
            chunks = self.chunk_text(text, chunk_size, overlap)
            
            for i, chunk in enumerate(chunks):
                # Generate embedding
                embedding = self.model.encode(chunk).tolist()
                
                # Create point
                points.append(
                    models.PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embedding,
                        payload={
                            "document": name,
                            "chunk_id": i,
                            "text": chunk
                        }
                    )
                )
        
        # Add to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        print(f"Added {len(points)} chunks from {len(documents)} documents")
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Retrieve relevant chunks for a query
        
        Args:
            query: The query text
            k: Number of results to return
        
        Returns:
            List of relevant chunks with metadata
        """
        query_vector = self.model.encode(query).tolist()
        
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=k
        )
        
        results = []
        for result in search_results:
            data = result.payload
            data["score"] = result.score
            results.append(data)
        
        return results