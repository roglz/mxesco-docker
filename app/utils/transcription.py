import whisper

def transcriber(audio):
  print("Cargando modelo Whisper...")
  whisper_model = whisper.load_model("medium.en")
  text_transcription = whisper_model.transcribe(
    audio = audio,
    condition_on_previous_text = False,
    word_timestamps = True,
    task = 'transcribe',
    language = 'en',
  )
  return text_transcription