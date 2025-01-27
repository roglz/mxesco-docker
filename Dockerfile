FROM pytorch/pytorch:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    git \
    espeak-ng \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for the FastAPI application (default is 8000)
EXPOSE 8000

# Default command to start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]