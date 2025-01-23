def add_pause_timestamp(words):
  pauses_list = []
  prev_end = 0
  for word in words:
    if word['start'] != prev_end:
      pauses_list.append({'word': f'<pause>', 'start': prev_end, 'end': word['start']})
    pauses_list.append(word)
    prev_end = word['end']
  return pauses_list

def offset_to_timestamp(offset, sampling_rate, downsampling_rate):
    timestamp = offset / (sampling_rate / downsampling_rate)
    return timestamp