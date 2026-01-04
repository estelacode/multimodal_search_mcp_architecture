import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import logging

logger = logging.getLogger(__name__)

class ChromaDatabase:
    def __init__(self, host: str, port: int, collection_name: str):
        """
        Initialize the ChromaDatabase object.

        Args:
            host (str): The host name of the ChromaDB server.
            port (int): The port number of the ChromaDB server.
            collection_name (str): The name of the ChromaDB collection.

        Returns:
            None
        """
        logger.info(f"Initializing ChromaDatabase with host: {host}, port: {port}, collection_name: {collection_name}")
        self.client = chromadb.HttpClient(host=host, port=port)

        self.collection = self.client.get_collection(collection_name, 
                                                     embedding_function=OpenCLIPEmbeddingFunction(),
                                                     data_loader=ImageLoader())


    def text_to_image_search(self, text_query: str, n_results: int) -> str:
        """Search for images based on the text query.

        Args:
            text_query (str): The text query.
            n_results (int): The number of results to retrieve.

        Returns:
            str: response with retrieved images and their metadata.
        """
        logger.info(f"Text to Image Search: {text_query}")
        return self.collection.query(query_texts=[text_query], include=['data', 'metadatas','uris','distances'], n_results=n_results)

    def image_to_image_search(self, image_query: str, n_results: int) -> str:
        """Search for images based on the image query.

        Args:
            image_query (str): The image query.
            n_results (int): The number of results to retrieve.

        Returns:
            str: response with retrieved images and their metadata.
        """
        logger.info(f"Image to Image Search")
        return self.collection.query(query_images=[image_query], include=['data','metadatas','uris','distances'], n_results=n_results)
