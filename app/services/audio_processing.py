import io
import os
import json
from datetime import datetime

from pydub import AudioSegment
import torch
import torchaudio

from app.utils.transcription import transcriber
from app.utils.phonemization import phonemizer
from app.services.corpus_app import corpus_app

def get_audio_duration(file_path, milliseconds=False):
    audio = AudioSegment.from_file(file_path)
    if milliseconds:
      duration = len(audio)
    else:
      duration = len(audio) / 1000
    return duration

def waveform_loader(file_path):
  waveform, sample_rate = torchaudio.load(file_path)
  if waveform.shape[0] == 2:
    waveform = torch.mean(waveform, dim=0, keepdim=True).squeeze()
  else:
    waveform = waveform.squeeze()
  return waveform, sample_rate

def process_audio(audio_bytes, filename):
    # Convertir bytes en waveform y sample_rate
    waveform, sample_rate = waveform_loader(io.BytesIO(audio_bytes))

    # Transcribir y fonemizar el audio
    text_transcription = transcriber(audio=waveform)
    phoneme_transcription = phonemizer(audio=waveform, sample_rate=sample_rate)

    # Generar JSON con corpus_app
    words_list = corpus_app(text_transcription, phoneme_transcription)
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