from setuptools import setup, find_packages

setup(
    name="frontend",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),  # Encuentra automáticamente todos los paquetes y subpaquetes
    install_requires=[
        # Lista de dependencias del proyecto:
        'gradio==6.2.0',
        'strands-agents==1.21.0',
        'python-dotenv==1.2.1',
        'faster-whisper==1.2.1',
        'soundfile==0.12.1',
    ],
)
