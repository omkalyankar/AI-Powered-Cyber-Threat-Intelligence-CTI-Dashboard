from qdrant_client import QdrantClient
import os

client = QdrantClient(url="http://qdrant:6333")
COL="iocs"
# Create collection if not exists
if COL not in [c.name for c in client.get_collections().collections]:
    client.recreate_collection(collection_name=COL, vector_size=384, distance="Cosine")
