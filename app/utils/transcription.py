import whisper

def transcriber(audio: any) -> dict:
    """
    Transcribes an audio waveform into text with word-level timestamps using the Whisper model.

    Args:
        audio (any): The input audio waveform. Typically a numpy array, PyTorch tensor, or other format supported by Whisper.

    Returns:
        dict: A dictionary containing the transcription text and word-level timestamps.
    """
    print("Loading Whisper model...")

    # Load the Whisper model
    whisper_model = whisper.load_model("medium.en")

    # Transcribe the audio with word timestamps
    text_transcription: dict = whisper_model.transcribe(
        audio=audio,
        condition_on_previous_text=False,
        word_timestamps=True,
        task='transcribe',
        language='en',
    )

    return text_transcription

"""
======================
This module provides functionality for transcribing audio waveforms into text with word-level 
timestamps using OpenAI's Whisper model.

Main Function:
- `transcriber`: Handles the transcription of audio data and returns a detailed result.

Workflow:
1. Load the Whisper model using the `whisper.load_model` method.
2. Transcribe the audio waveform with word timestamps enabled.
3. Return the transcription result as a dictionary with detailed metadata.

Dependencies:
- `whisper`: OpenAI's library for speech recognition and transcription.

Example Usage:
======================
1. Prepare an audio waveform (e.g., using PyTorch or NumPy).
2. Call the `transcriber` function with the audio waveform as input.

Expected Output:
- The output is a dictionary containing:
  - The full transcription text.
  - Detailed segments, including word-level timestamps.

Performance Notes:
- The model `medium.en` is optimized for English transcription and provides word-level timestamps.
- Ensure the input audio matches the supported formats for Whisper (e.g., mono, specific sampling rates).

"""
