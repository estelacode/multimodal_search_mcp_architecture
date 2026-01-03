# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /mcp_server

# Copia los archivos del proyecto (el código de tu MCP server)
COPY . /mcp_server

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto donde el MCP Server estará disponible
EXPOSE 9000  

# Comando para ejecutar el MCP server
CMD ["python", "main.py"]  
