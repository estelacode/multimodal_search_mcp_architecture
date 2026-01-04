
from mcp.client.streamable_http import streamable_http_client
from strands.tools.mcp import MCPClient
from strands.tools.mcp.mcp_types import MCPToolResult
from frontend.utils import base64_to_pil_image
from typing import Any
import uuid
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()


class MultimodalSearchMCPClient:
    
    @staticmethod
    def create_mcp_client() -> MCPClient:
        """
        Creates and returns an MCPClient instance.

        Returns:
            MCPClient: An instance of MCPClient connected to the specified MCP server.
        """
        logger.info("Creating MCPClient instance")
        return MCPClient(lambda: streamable_http_client(os.getenv("MCP_SERVER_URL")))
    
    @staticmethod
    def get_tools(mcp_client: MCPClient) -> list[str]:
        
        """
        Fetches the list of available tools from the MCPClient.
        Args:
            mcp_client (MCPClient): The MCPClient instance to use.

        Returns:
            list[str]: A list of tool names available on the MCPClient.
        """
        logger.info("Fetching tools from MCPClient")
        return [tool.tool_name for tool in mcp_client.list_tools_sync()]
    
    @staticmethod
    def invoke_tool(mcp_client: MCPClient,tool_name: str, arguments: dict[str, Any])-> MCPToolResult:
        
        """
        Calls a tool on the MCPClient with the given arguments.

        Args:
            mcp_client (MCPClient): The MCPClient instance to use.
            tool_name (str): The name of the tool to call.
            arguments (dict[str, Any]): The arguments to pass to the tool.

        Returns:
            dict: The response from the MCPClient.
        """
        logger.info("Calling tool '%s' on MCPClient with arguments: %s", tool_name, arguments)
        return mcp_client.call_tool_sync(tool_use_id=str(uuid.uuid4()), name=tool_name, arguments=arguments)

    @staticmethod
    def get_items_gallery(result:MCPToolResult)-> list:
      
        """
        Transforms the given MCPToolResult into a list of gallery items.

        Each item in the list is a tuple containing a PIL image and a caption string.

        The caption string is formatted as follows: "{name} — ${price} — {category}"

        If an error occurs during processing, an empty list is returned and the error is logged.

        Args:
            result (MCPToolResult): The MCPToolResult to process.

        Returns:
            list: A list of gallery items.
        """
        try:
            logger.info("Transforming MCPToolResult into gallery items")
            structured_content = result["structuredContent"]
            items = structured_content["result"]
            gallery_items = []
            
            for item in items:
                
                meta = item["metadata"]
                caption = f"{meta['name']} — ${meta['price']} — {meta['category']}"
                base64_img = meta['base64_image']
                image= base64_to_pil_image(base64_img)
                gallery_items.append([image, caption])
            logger.info("Successfully created %d gallery items", len(gallery_items))
            return gallery_items
        except Exception as e:
            logger.error("Error processing gallery items: %s", e)
            return []
