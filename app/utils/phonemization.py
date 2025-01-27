import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

def phonemizer(audio: torch.Tensor, sample_rate: int) -> list[dict]:
    """
    Phonemizes an audio waveform by converting it into a sequence of phonemes with character offsets.

    Args:
        audio (torch.Tensor): The audio waveform as a PyTorch tensor. Typically a 1D tensor for mono audio.
        sample_rate (int): The sample rate of the audio in Hz.

    Returns:
        list[dict]: A list of character offsets with phoneme information. Each dictionary contains:
            - 'char': The predicted character or phoneme.
            - 'start_offset': The starting offset of the character in the audio.
    """
    print("Loading Wav2Vec model...")

    # Load the Wav2Vec2 processor and model
    wav2vec_processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft")
    wav2vec_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft")
    
    # Convert the audio waveform into input values for the Wav2Vec2 model
    input_values = wav2vec_processor(audio, return_tensors="pt", sampling_rate=sample_rate).input_values

    # Perform inference to get logits (model output)
    with torch.no_grad():
        logits = wav2vec_model(input_values).logits

    # Decode logits to predicted character IDs
    predicted_ids = torch.max(logits, dim=-1).indices

    # Decode the predicted IDs to characters and obtain character offsets
    decoded_ids = wav2vec_processor.batch_decode(predicted_ids, output_char_offsets=True)

    # Extract character offsets from the decoded output
    char_offsets = decoded_ids['char_offsets'][0]

    return char_offsets

"""
======================
This module provides functionality for phonemizing audio waveforms using the Wav2Vec2 model
pretrained with Espeak.

Main Function:
- `phonemizer`: Converts an audio waveform into phonemes with character offsets.

Workflow:
1. Load the Wav2Vec2 processor and model from the Hugging Face Transformers library.
2. Convert the audio waveform into input values required by the model.
3. Perform inference on the input values to obtain logits.
4. Decode logits into phonemes with character offsets using the processor.

Dependencies:
- `transformers`: Provides the Wav2Vec2 model and processor.
- `torch`: Used for tensor computations and managing model inference.

Example Usage:
======================
1. Load a mono audio waveform using PyTorch or Torchaudio.
2. Call the `phonemizer` function with the waveform and sample rate.

Output:
The function returns a list of dictionaries, where each dictionary contains:
    - 'char': The predicted character or phoneme.
    - 'start_offset': The timestamp (in samples) where the character begins in the audio.

Performance Notes:
- The pretrained model ("facebook/wav2vec2-xlsr-53-espeak-cv-ft") is optimized for phoneme transcription.
- Ensure the input audio is mono and matches the sample rate of the model.
"""
