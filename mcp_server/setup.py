from setuptools import setup, find_packages

setup(
    name="mcp_server",
    version="0.1.0",
    package_dir={"": "src"}, # Indica que los paquetes están en el directorio 'src' 
    packages=find_packages(where="src"),  # Encuentra automáticamente todos los paquetes y subpaquetes
    install_requires=[
        # Lista de dependencias del proyecto:
        'chromadb==1.3.5',
        'fastmcp==2.13.3',
        'pandas==2.3.3',
        'numpy==2.3.5',
        'pillow==12.0.0',
        'open_clip_torch==3.2.0',
        'python-dotenv==1.2.1',
    ],
)
