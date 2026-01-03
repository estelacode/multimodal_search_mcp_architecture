# MCP Server App 

## 1. Create the virtual environment
```bash
py -3.12 -m venv .venv
```

## 2. Activate the virtual environment
```bash
.venv\Scripts\activate
where python # Confirm the virtual environment is active by checking the Python interpreter location
deactivate # Use this to deactivate the environment
```

## 3. Install dependencies
```bash
pip install chromadb
pip install fastmcp
pip install pandas
pip install numpy
pip install pillow
pip install open-clip-torch
```

## 4. Create the setup.py file
Create a file named setup.py in the project root with the following content:
```bash
# This enables packaging and installation of the project located inside the src/ directory
from setuptools import setup, find_packages

setup(
    name="mcp_server",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
```
## 5. Install the project in editable mode
This allows us to modify the source code and have changes applied immediately without reinstalling the package.
```bash
pip install -e .  # After creating the setup.py file, run:
```


## 6. MCP Inspector
```bash
# Run the Model Context Protocol Inspector with:
npx @modelcontextprotocol/inspector
```

# Devops

## 1. Create Docker Image
```bash 
docker build -t mcp_server .
```

## 2. List all created Docker Images
```bash
docker images
```

## 3. Create and run a container from the created image
```bash
docker run -d -p 9000:9000 --name mcp_server_container mcp_server
```

## 4. List all created Docker containers
```bash
docker ps
```

## 5. Access to the mcp_server_container 
```bash 
http://localhost:9000/mcp
```