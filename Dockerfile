# Usa una imagen oficial de Python
FROM python:3.11

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia y actualiza pip antes de instalar dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    pip install gunicorn  # <-- Forzamos la instalación de Gunicorn

# Copia el código de la aplicación Django al contenedor
COPY . /app/

# Exponer el puerto donde correrá Gunicorn
EXPOSE 8000

# Verificar que gunicorn se instaló
#RUN pip list | grep gunicorn || exit 1  # <-- Si Gunicorn no se instala, el build falla

# Comando por defecto para iniciar Django con Gunicorn
CMD ["gunicorn", "sitio.wsgi:application", "--bind", "0.0.0.0:8000"]
