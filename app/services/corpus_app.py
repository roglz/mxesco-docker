from app.utils.timestamps import offset_to_timestamp, add_pause_timestamp

def corpus_app(text_transcription, phoneme_transcription, sample_rate=16000, downsampling_rate=320):
  segment_list = [segment['words'] for segment in text_transcription['segments']]
  words_list = sum(segment_list, [])

  tokens_list = [segment['tokens'] for segment in text_transcription['segments']]
  tokens_list = sum(tokens_list, [])

  end_list = [0] + [word['end'] for word in words_list]

  phoneme_list = []
  for i in range(len(end_list)-1):
    phoneme = '/'
    for char in phoneme_transcription:
      char_timestamp = offset_to_timestamp(char['start_offset'], sample_rate, downsampling_rate)
      if end_list[i] <= char_timestamp < end_list[i+1]:
        phoneme += char['char']
    phoneme_list.append(phoneme+'/')

  prev_end = 0
  for word, token, phoneme in zip(words_list, tokens_list, phoneme_list):
    word['token_id'] = token
    word['phoneme'] = phoneme

  words_list = add_pause_timestamp(words_list)

  return words_list