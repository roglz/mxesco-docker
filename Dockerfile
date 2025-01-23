# Usa la imagen base de PyTorch con soporte para CUDA, si es necesario
FROM pytorch/pytorch:latest

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el contenido del proyecto al contenedor
COPY . /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    git \
    espeak-ng \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar las dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto (por ejemplo, para la API FastAPI)
EXPOSE 8000

# Comando predeterminado para iniciar la aplicación (ajústalo según lo que necesites)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]