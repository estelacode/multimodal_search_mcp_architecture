# Low Latency Multimodal Search Web App with MCP Architecture

## Introduction

The goal of this project is to build a web application for multimodal search using an MCP (Multimodal Conversational Platform) architecture. The solution allows users to perform queries via voice, text, or image over a database of footwear images and their metadata. Through this application, users can search for products (e.g., footwear) and get relevant results based on different query modalities.

## Goal

The main goal of this project is to demonstrate how a multimodal search system can benefit from MCP architecture and how libraries like faster-whisper improve the latency of audio-to-text conversion compared to OpenAI's Whisper models

## Tech Stack

![Python](https://img.shields.io/badge/Python-white?style=for-the-badge&logo=python&logoColor=8d98f0&color=8d98f0&labelColor=F3F4F6)
![MCP Server](https://img.shields.io/badge/MCP_Server-white?style=for-the-badge&logo=modelcontextprotocol&logoColor=8d98f0&color=8d98f0&labelColor=F3F4F6)
![MCP Protocol](https://img.shields.io/badge/MCP-Protocol-white?style=for-the-badge&logo=mcp-protocol&logoColor=8d98f0&color=8d98f0&labelColor=F3F4F6)
![Strands Agent SDK](https://img.shields.io/badge/sdk-strands_agents-white?style=for-the-badge&logo=sdk-strands-agents&logoColor=8d98f0&color=8d98f0&labelColor=F3F4F6)
![OpenAI Whisper](https://img.shields.io/badge/OpenAI-Whisper-white?style=for-the-badge&logo=openai-whisper&logoColor=8d98f0&color=8d98f0&labelColor=F3F4F6)
![Faster-Whisper](https://img.shields.io/badge/Faster_Whisper-white?style=for-the-badge&logo=python&logoColor=8d98f0&color=8d98f0&labelColor=F3F4F6)
![ChromaDB](https://img.shields.io/badge/ChromaDB-white?style=for-the-badge&logo=databricks&logoColor=8d98f0&color=8d98f0&labelColor=F3F4F6)
![Gradio](https://img.shields.io/badge/Gradio-white?style=for-the-badge&logo=gradio&logoColor=8d98f0&color=8d98f0&labelColor=F3F4F6)

* **Gradio UI** for the frontend interface.
* **Docker** for containerization and deployment.
* **MCP Client/Server** communication via the **MCP protocol**.
* **ChromaDB** for efficient vector-based search and retrieval.
* **faster-whisper** for Speech-to-Text conversion.


# Project Structure
The project is organized in a modular architecture to ensure clear separation of concerns:
```bash
MULTIMODAL_SEARCH_MCP_ARCHITECTURE/
├── frontend/                        # Frontend application directory
│   ├── .venv                        # Virtual environment for frontend dependencies
│   ├── .env                         # Environment variables for frontend
│   ├── .env.example                 # Example environment variables for frontend
│   ├── src                          # Source code for the frontend application
│   ├── .dockerignore                # Files to exclude from Docker container (for frontend)
│   ├── main.py                      # Main entry point for the frontend application
│   ├── setup.py                     # Setup script for frontend dependencies
│   ├── requirements.txt             # List of Python dependencies for the frontend
│   ├── Dockerfile                   # Container configuration for the frontend
│   └── README.md                    # Documentation for the frontend
│
├── mcp_server/                      # MCP server application directory
│   ├── .venv                        # Virtual environment for server dependencies
│   ├── .env                         # Environment variables for the MCP server
│   ├── .env.example                 # Example environment variables for MCP server
│   ├── src                          # Source code for the MCP server
│   ├── .dockerignore                # Files to exclude from Docker container (for MCP server)
│   ├── main.py                      # Main entry point for the MCP server application
│   ├── setup.py                     # Setup script for MCP server dependencies
│   ├── requirements.txt             # List of Python dependencies for the MCP server
│   ├── Dockerfile                   # Container configuration for the MCP server
│   └── README.md                    # Documentation for the MCP server
│
├── chroma_db/                       # Directory for ChromaDB (Vector database) data
│   ├── 63cee2db-cf31-45f0-a9e0-8dcdc99ca54d # Sample or unique ID related to data in ChromaDB
│   └── chroma.sqlite3               # ChromaDB database file
│
├── .gitignore                       # Files and directories to exclude from version control (global)
├── docker-compose.yml               # Docker Compose configuration to manage all containers
└── README.md                        # Main project documentation

```


# Devops

The Dockerfile files for both frontend and mcp_server configure how each service runs inside a Docker container.
The docker-compose.yml is used to orchestrate the services for the entire project, ensuring that the frontend, mcp_server, and chroma_db work together seamlessly in Docker containers.

```bash
docker-compose up 
```