import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader



client = chromadb.PersistentClient("C:/Users/emada/Desktop/ia_workspace/multimodal_search_mcp_architecture/chroma_db")

collection = client.get_collection("men_shoes")
print(f"✅ Collection 'men_shoes' loaded. Embeddings: {collection.count()}")


