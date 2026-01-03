# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /mcp_server

# Copiar el archivo setup.py y requirements.txt al contenedor
COPY setup.py requirements.txt /mcp_server/

# Instalar las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Instalar el paquete de la aplicación en modo editable
RUN pip install --no-cache-dir -e .

# Copia el resto de los archivos del proyecto
COPY . /mcp_server/

# Exponer el puerto donde el MCP Server estará disponible
EXPOSE 9000  

# Comando para ejecutar el MCP server
CMD ["python", "main.py"]
