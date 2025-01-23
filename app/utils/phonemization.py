import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

def phonemizer(audio, sample_rate):
  print("Cargando modelo Wav2Vec...")

  wav2vec_processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft")
  wav2vec_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft")
  input_values = wav2vec_processor(audio, return_tensors="pt", sampling_rate=sample_rate).input_values

  with torch.no_grad():
    logits = wav2vec_model(input_values).logits

  predicted_ids = torch.max(logits, dim=-1).indices
  decoded_ids = wav2vec_processor.batch_decode(predicted_ids, output_char_offsets=True)

  char_offsets = decoded_ids['char_offsets'][0]

  return char_offsets