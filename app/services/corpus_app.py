from app.utils.timestamps import offset_to_timestamp, add_pause_timestamp

def corpus_app(
    text_transcription: dict, 
    phoneme_transcription: list[dict], 
    sample_rate: int = 16000, 
    downsampling_rate: int = 320
) -> list[dict]:
    """
    Processes transcription and phoneme data to enrich word metadata with tokens, phonemes, 
    and timestamps.

    Args:
        text_transcription (dict): The text transcription data containing word segments and tokens.
        phoneme_transcription (list[dict]): A list of phonemes with their character and start offset.
        sample_rate (int, optional): The sample rate of the audio in Hz. Defaults to 16000.
        downsampling_rate (int, optional): The rate at which phoneme timestamps are downsampled. Defaults to 320.

    Returns:
        list[dict]: A list of enriched word dictionaries with token IDs, phonemes, and pause timestamps.
    """
    # Extract word segments from transcription data
    segment_list: list[list[dict]] = [segment['words'] for segment in text_transcription['segments']]
    words_list: list[dict] = sum(segment_list, [])  # Flatten the list of words

    # Extract token IDs from transcription data
    tokens_list: list[list[int]] = [segment['tokens'] for segment in text_transcription['segments']]
    tokens_list: list[int] = sum(tokens_list, [])  # Flatten the list of tokens

    # Generate a list of word end times
    end_list: list[float] = [0] + [word['end'] for word in words_list]

    # Initialize the list of phonemes
    phoneme_list: list[str] = []
    for i in range(len(end_list) - 1):
        phoneme = '/'  # Start phoneme string with '/'
        for char in phoneme_transcription:
            # Convert character offsets to timestamps
            char_timestamp = offset_to_timestamp(char['start_offset'], sample_rate, downsampling_rate)
            # Append character to phoneme if it falls within the word's time range
            if end_list[i] <= char_timestamp < end_list[i + 1]:
                phoneme += char['char']
        phoneme_list.append(phoneme + '/')  # End phoneme string with '/'

    # Add token IDs and phonemes to the corresponding words
    prev_end = 0
    for word, token, phoneme in zip(words_list, tokens_list, phoneme_list):
        word['token_id'] = token
        word['phoneme'] = phoneme

    # Add pause timestamps between words
    words_list = add_pause_timestamp(words_list)

    return words_list

"""
======================
This module processes text transcription and phoneme transcription data to generate enriched 
metadata for words, including phonemes, token IDs, and pause timestamps.

Functions:
- `corpus_app`: The main function to process and enrich transcription data.

Workflow:
1. Extract word segments and tokens from the transcription data.
2. Calculate phoneme ranges using phoneme timestamps and word end times.
3. Enrich each word with its corresponding token ID and phoneme sequence.
4. Add pause timestamps between words to indicate silences.

Dependencies:
- `offset_to_timestamp`: Converts phoneme offsets to actual timestamps.
- `add_pause_timestamp`: Adds pause timestamps to the list of words.

Example Usage:
======================
Input Data:
    text_transcription = {
        "segments": [
            {
                "words": [{"start": 0.0, "end": 1.0, "text": "hello"}],
                "tokens": [101]
            }
        ]
    }
    phoneme_transcription = [
        {"char": "h", "start_offset": 0},
        {"char": "e", "start_offset": 1000}
    ]

Function Call:
    words_list = corpus_app(text_transcription, phoneme_transcription)

Expected Output:
    [
        {
            "start": 0.0,
            "end": 1.0,
            "text": "...",
            "token_id": 101,
            "phoneme": "/.../",
            "pause_start": 1.0,
            "pause_end": 1.5
        }
    ]
"""