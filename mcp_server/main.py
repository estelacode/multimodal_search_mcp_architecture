
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
chroma_db = ChromaDatabase(host=os.getenv("CHROMADB_HOST"), port=os.getenv("CHROMADB_PORT"), collection_name=os.getenv("CHROMADB_COLLECTION_NAME"))

# Create mcp server instance
mcp = FastMCP(name=os.getenv("MCP_SERVER_NAME"), port=os.getenv("MCP_SERVER_PORT"))


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

    uris = result["uris"][0]
    metadatas = result["metadatas"][0]
    data = result["data"][0]

    return [
        {   
            # Original location of the image (not used in the frontend currently)
            "uri": uris[i],
            # Metadata associated with the image
            "metadata": metadatas[i],
            # Matrix of pixel values converted to base64 string
            "data": ndarray_to_base64(data[i])
        }
        for i in range(len(uris))
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
        logger.debug(f"Text to Image Search Result: {result}")

        # Check if there are URIs and metadata in the result
        uris = result["uris"][0]
        metadatas = result["metadatas"][0]
        data = result["data"][0]
        

        # Check for missing URIs or metadata or data
        if not data:
            logger.warning(f"No data found for query: '{text_query}'.")
        if not uris:
            logger.warning(f"No URIs found for query: '{text_query}'.")
        if not metadatas:
            logger.warning(f"No metadata found for query: '{text_query}'.")

        # If no URIs or metadata, return an empty list or raise an exception
        if not uris or not metadatas:
            logger.error(f"Search for query '{text_query}' did not return valid results.")
            return []  # Return empty list or handle accordingly

        # Convert image data (pixel matrix) to base64 and include in the response
        return [
            {   
                # Original location of the image (not used in the frontend currently)
                "uri": uris[i],
                # Metadata associated with the image
                "metadata": metadatas[i],
                # Matrix of pixel values converted to base64 string
                "data": ndarray_to_base64(data[i])
            }
            for i in range(len(uris))
        ]
    
    except Exception as e:
        logger.error(f"An error occurred during the text-to-image search for query '{text_query}': {e}")
        return []  # Return empty list or handle the error as needed
            

if __name__ == "__main__":
    print("🚀 Launching MCP Server...")
    mcp.run(transport="streamable-http")
    

