# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /frontend

# Copiar el archivo setup.py y requirements.txt al contenedor
COPY setup.py requirements.txt /frontend/

# Instalar las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos del proyecto
COPY . /frontend/

# Instalar el paquete de la aplicación en modo editable
RUN pip install -e .

# Exponer el puerto donde el frontend estará disponible
EXPOSE 3000 

# Comando para ejecutar el frontend
CMD ["python", "main.py"]
