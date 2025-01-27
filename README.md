# MXESCO-DOCKER

MXESCO-DOCKER is a robust and modular application designed for processing audio files. It includes features for transcription, phonemization, metadata generation, and storage in a MongoDB database. Built with FastAPI, it leverages advanced libraries such as OpenAI's Whisper and Hugging Face's Wav2Vec2 for speech and phoneme recognition.

## Features
- **Audio Transcription**: Extracts text from audio files with word-level timestamps.
- **Phonemization**: Converts audio data into phonemes with detailed character offsets.
- **Metadata Generation**: Includes information about the transcriber model, phonemizer, and timestamps.
- **Data Storage**: Stores processed data and raw audio in MongoDB using GridFS.
- **REST API**: Exposes endpoints for uploading and processing audio files.
- **Containerization**: Dockerized for ease of deployment.

## Project Structure
```
MXESCO-DOCKER/
├── app/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── audio_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── audio_processing.py
│   │   ├── corpus_app.py
│   │   ├── database.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── phonemization.py
│   │   ├── timestamps.py
│   │   ├── transcription.py
│   ├── main.py
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
```

### Key Files
- **`main.py`**: Entry point for the FastAPI application.
- **`audio_routes.py`**: Defines API endpoints for processing audio files.
- **`audio_processing.py`**: Handles transcription, phonemization, and metadata generation.
- **`database.py`**: Saves metadata and audio files to MongoDB.
- **`corpus_app.py`**: Processes word and phoneme data for enriched metadata.
- **`utils/`**: Utility functions for timestamps, transcription, and phonemization.

## Installation

### Prerequisites
- Docker and Docker Compose installed
- Python 3.9+

### Steps
1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd mxesco-docker
    ```
2. Build and run the Docker containers:
    ```bash
    docker compose up --build
    ```
3. The API will be available at [http://localhost:8000](http://localhost:8000).

### Running Locally Without Docker
1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2. Start the FastAPI server:
    ```bash
    uvicorn app.main:app --reload
    ```

## Usage

### API Endpoints

#### Process Audio File
- **Endpoint**: `/api/process-audio/`
- **Method**: `POST`
- **Description**: Uploads an audio file for processing.
- **Example Request**:
    ```bash
    curl -X POST "http://127.0.0.1:8000/api/process-audio/" \
         -F "file=@example_audio.mp3"
    ```
- **Response**:
    ```json
    {
        "status": "success",
        "message": "Audio processed and saved successfully."
    }
    ```

### Interactive API Documentation
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Technologies Used
- **FastAPI**: Web framework for building APIs.
- **PyTorch**: For handling audio data and Wav2Vec2 model inference.
- **Whisper**: OpenAI's speech-to-text library.
- **MongoDB & GridFS**: For data persistence.
- **Docker**: For containerized deployment.
- **Pydub**: For audio file manipulation.
- **Phonemizer**: For generating phonemes from text.

## Configuration

### Docker
- **`docker-compose.yml`**:
    - Defines two services:
        1. `app`: The FastAPI application.
        2. `mongo`: MongoDB database.
    - Exposes ports `8000` for the application and `27017` for MongoDB.

### Environment Variables
To customize settings, modify the environment variables in the `docker-compose.yml` file or create a `.env` file.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

## Acknowledgements
- OpenAI for Whisper
- Hugging Face for Wav2Vec2
- MongoDB for efficient data handling
- Maestría en Ciencia de Datos, Universidad de Sonora ([GitHub Repository](https://github.com/mcd-unison))
