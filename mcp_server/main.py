
from fastmcp import FastMCP
from mcp_server.utils import image_to_base64, base64_to_ndarray, ndarray_to_base64
from mcp_server.db import ChromaDatabase
from typing import List, Dict
import logging
import os
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO, 
    # time in a human-readable format, the severity of the message, and the message content
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(), # display the logs in the console
        logging.FileHandler("mcp_server.log") # saves the logs into a file
    ]
)

logger = logging.getLogger(__name__)


load_dotenv()  

# Initialize ChromaDB connection
chroma_db = ChromaDatabase(host=os.getenv("CHROMADB_HOST"), port=int(os.getenv("CHROMADB_PORT")), collection_name=os.getenv("CHROMADB_COLLECTION_NAME"))

# Create mcp server instance
mcp = FastMCP(name=os.getenv("MCP_SERVER_NAME"), port=int(os.getenv("MCP_SERVER_PORT")))


@mcp.tool
def image_to_image_search_tool(image_query:str,top_k: int)-> List[Dict]:
    """
    Perform an image to image search using the provided ChromaDB collection.
    Args:
       
        image_query (str):  base64-encoded string of the query image.
        top_k (int): The number of top results to retrieve.

    Returns:
        List[Dict]: list: a list of items each containing 'data' and 'metadata'.
    """
    logger.info(f"Calling 'image_to_image_search' with top_k: {top_k}")
    # Convert the base64-encoded image to a NumPy array
    image_query_array = base64_to_ndarray(image_query)
    # Perform the image to image search
    result = chroma_db.image_to_image_search( image_query_array, n_results=top_k)
    logger.debug(f"Image to Image Search Result: {result}")

    metadatas = result["metadatas"][0]
    return [
        {   
            # Metadata associated with the image
            "metadata": metadatas[i],
            # Matrix of pixel values converted to base64 string
            "base64_image": metadatas[i]['base64_image']
        }
        for i in range(len(metadatas))
    ]  
    

@mcp.tool
def text_to_image_search_tool(text_query: str, top_k: int)-> List[Dict]:

    """
    Perform a text to image search using the provided ChromaDB collection.
    
    Args:
        
        text_query (str): The text query.
        top_k (int): The number of top results to retrieve.
    
    Returns:
        List[Dict]: list: a list of items each containing 'uri' and 'metadata'.
    """
    logger.info(f"Calling 'text_to_image_search' with query: '{text_query}' and top_k: {top_k}")

    # Perform the search
    try:
        result = chroma_db.text_to_image_search(text_query, n_results=top_k)
        logger.info(f"Text to Image Search Result: {result}")

        # Check if there are URIs and metadata in the result
        metadatas = result["metadatas"][0]
    
        return [
            {   
                # Metadata associated with the image
                "metadata": metadatas[i],
                # Matrix of pixel values converted to base64 string
                "base64_image": metadatas[i]['base64_image']
            }
            for i in range(len(metadatas))
        ]
    
    except Exception as e:
        logger.error(f"An error occurred during the text-to-image search for query '{text_query}': {e}")
        return []  # Return empty list or handle the error as needed
            

if __name__ == "__main__":
    print("🚀 Launching MCP Server...")
    mcp.run(transport="streamable-http",   port=int(os.getenv("MCP_SERVER_PORT")), host=os.getenv("MCP_SERVER_HOST"))
    

