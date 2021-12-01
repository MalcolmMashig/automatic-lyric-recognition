# modulate-training-data.py

import soundfile as sf
from pydub import AudioSegment
import os
import numpy as np

flac_path = "mini-librispeech/dev-clean/1272/135031/1272-135031-0021.flac"
wav_path = "mini-librispeech/dev-clean/1272/135031/1272-135031-0021.wav"

# read .flac (mini-LibriSpeech development dataset)
eg_flac, eg_sr = sf.read(flac_path)

# convert to .wav
sf.write(wav_path, eg_flac, eg_sr)

# delete original .flac
os.remove(flac_path)

# read .wav
eg_wav = AudioSegment.from_file(wav_path)

# determine modulation
rand_mod = np.random.randint(2, size = 1)
if rand_mod[0] == 1:
  modulation = np.random.uniform(0.8,0.9,1)
else:
  modulation = np.random.uniform(1.1,1.25,1)

# n chunks to modulate per file (should be even)
n_chunks = 4

eg_wav_length = eg_wav.duration_seconds

split = eg_wav_length / n_chunks

combined = eg_wav[0:0]
for i in range(0, (n_chunks)):
  timemark = np.arange(split, (eg_wav_length + split), split)[i]
  chunk = eg_wav[(timemark*1000 - (split*1000)):(timemark*1000)]
  if ((i % 2) == 0):
    chunk_mod = chunk._spawn(chunk.raw_data, overrides={
         "frame_rate": int(chunk.frame_rate * modulation)
      })
    chunk_mod = chunk_mod.set_frame_rate(chunk.frame_rate)
  else:
    chunk_mod = chunk._spawn(chunk.raw_data, overrides={
           "frame_rate": int(chunk.frame_rate * (1/modulation)) # inverse
        }).set_frame_rate(chunk.frame_rate)
    chunk_mod = chunk_mod.set_frame_rate(chunk.frame_rate)
  combined += chunk_mod

# delete intermediate .wav
os.remove(wav_path)

# save as .flac
combined.export(flac_path, format = "flac")

