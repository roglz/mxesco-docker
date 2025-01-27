def add_pause_timestamp(words: list[dict]) -> list[dict]:
    """
    Adds pause timestamps between words in a list of word metadata.

    Args:
        words (list[dict]): A list of dictionaries, where each dictionary represents a word with 
                            its start and end timestamps.

    Returns:
        list[dict]: A new list of word dictionaries with added `<pause>` entries for silent periods.
    """
    pauses_list: list[dict] = []
    prev_end: float = 0.0

    for word in words:
        # Check for a gap between the previous word's end and the current word's start
        if word['start'] != prev_end:
            pauses_list.append({'word': '<pause>', 'start': prev_end, 'end': word['start']})

        # Append the current word to the list
        pauses_list.append(word)

        # Update the previous end timestamp
        prev_end = word['end']

    return pauses_list


def offset_to_timestamp(offset: int, sampling_rate: int, downsampling_rate: int) -> float:
    """
    Converts a character offset to a timestamp based on sampling and downsampling rates.

    Args:
        offset (int): The character offset to convert.
        sampling_rate (int): The original sampling rate of the audio in Hz.
        downsampling_rate (int): The downsampling rate applied during processing.

    Returns:
        float: The corresponding timestamp in seconds.

    Formula:
        timestamp = offset / (sampling_rate / downsampling_rate)
    """
    timestamp: float = offset / (sampling_rate / downsampling_rate)
    return timestamp

"""
======================
This module provides utility functions for handling word timestamps and pauses in transcribed audio data.

Functions:
- `add_pause_timestamp`: Detects silent gaps between words and inserts pause entries into a list of word metadata.
- `offset_to_timestamp`: Converts a character offset to a timestamp based on audio sampling and downsampling rates.

Usage:
1. Use `add_pause_timestamp` to enrich a word metadata list by adding `<pause>` entries for silent periods.
2. Use `offset_to_timestamp` to map character offsets (e.g., phoneme positions) to timestamps in seconds.

Example Workflow:
======================
1. Prepare a list of word dictionaries with `start` and `end` timestamps.
2. Call `add_pause_timestamp` to identify and mark pauses.
3. Use `offset_to_timestamp` to process offsets for phoneme or character timings.

Example Data:
======================
words = [
    {"text": "hello", "start": 0.0, "end": 1.0},
    {"text": "world", "start": 1.5, "end": 2.5},
]

Result:
[
    {"text": "hello", "start": 0.0, "end": 1.0},
    {"word": "<pause>", "start": 1.0, "end": 1.5},
    {"text": "world", "start": 1.5, "end": 2.5},
]

Performance Notes:
======================
- The `add_pause_timestamp` function assumes the input list is sorted by `start` timestamps.
- The `offset_to_timestamp` function uses the downsampling rate to calculate accurate timestamps, ensuring compatibility with processed audio data.
"""