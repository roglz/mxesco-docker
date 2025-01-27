import io
from datetime import datetime

from pydub import AudioSegment
import torch
import torchaudio

from app.utils.transcription import transcriber
from app.utils.phonemization import phonemizer
from app.services.corpus_app import corpus_app

def get_audio_duration(file_path: io.BytesIO, milliseconds: bool = False) -> float:
	"""
	Calculate the duration of an audio file.

	Args:
		file_path (io.BytesIO): The audio file to calculate the duration for.
		milliseconds (bool): If True, return duration in milliseconds. Defaults to False.

	Returns:
		float: Duration of the audio file in seconds or milliseconds.
	"""
	audio = AudioSegment.from_file(file_path)
	if milliseconds:
		duration = len(audio) # Duration in milliseconds
	else:
		duration = len(audio) / 1000 # Convert milliseconds to seconds
	return duration

def waveform_loader(file_path: io.BytesIO) -> tuple[torch.Tensor, int]:
    """
    Load the waveform and sample rate from an audio file.

    Args:
        file_path (io.BytesIO): The audio file to load.

    Returns:
        tuple[torch.Tensor, int]: A tuple containing the waveform tensor and its sampling rate.
    """
    waveform, sample_rate = torchaudio.load(file_path)
    
	# Convert stereo to mono if necessary
    if waveform.shape[0] == 2:
        waveform = torch.mean(waveform, dim=0, keepdim=True).squeeze()
    else:
        waveform = waveform.squeeze()
    return waveform, sample_rate

def process_audio(audio_bytes: bytes, filename: str) -> dict:
    """
    Process an audio file: transcribe, phonemize, and generate metadata.

    Args:
        audio_bytes (bytes): The raw audio file in bytes format.
        filename (str): The name of the audio file.

    Returns:
        dict: A dictionary containing metadata, transcriptions, and phoneme data.
    """
    # Convert audio bytes into waveform and sample rate
    waveform, sample_rate = waveform_loader(io.BytesIO(audio_bytes))

    # Transcribe the audio
    text_transcription = transcriber(audio=waveform)
    
	# Phonemize the audio
    phoneme_transcription = phonemizer(audio=waveform, sample_rate=sample_rate)

    # Generate a list of words using the corpus application
    words_list = corpus_app(text_transcription, phoneme_transcription)
    
	# Create a JSON-like dictionary with metadata and transcriptions
    json_dict = {
        'metadata': {
            'transcriber_model': 'medium.en',
            'phonemizer_model': 'facebook/wav2vec2-xlsr-53-espeak-cv-ft',
            'datetime': datetime.now().strftime('%d/%m/%Y, %H:%M:%S'),
        },
        'audio': {
            'file': filename,
            'duration': get_audio_duration(io.BytesIO(audio_bytes)),
            'sampling_rate': sample_rate,
        },
        'text_transcription': text_transcription['text'],
        'words': words_list,
    }
    return json_dict

"""
======================
This module handles audio file processing, including loading, transcribing, phonemizing, 
and generating metadata for audio files.

Functions:
- `get_audio_duration`: Calculates the duration of an audio file in seconds or milliseconds.
- `waveform_loader`: Converts raw audio bytes into a waveform tensor and retrieves the sample rate.
- `process_audio`: Processes audio files by transcribing, phonemizing, and generating a JSON-like dictionary with metadata.

External Dependencies:
- `pydub` for audio duration calculation.
- `torchaudio` for waveform loading and processing.
- Custom utilities for transcription (`transcriber`) and phonemization (`phonemizer`).
- A corpus application (`corpus_app`) to generate word lists.

Example Usage:
======================
Process an audio file:
    audio_bytes = open("example_audio.wav", "rb").read()
    result = process_audio(audio_bytes, "example_audio.wav")

Expected Output:
    {
        "metadata": {...},
        "audio": {...},
        "text_transcription": "Transcribed text...",
        "words": [...]
    }
"""