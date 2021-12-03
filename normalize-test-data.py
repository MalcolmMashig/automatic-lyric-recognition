# normalize-test-data.py

import os
import pydub
from pydub import AudioSegment
import glob
from glob import glob
import shutil
import re

# Isolate Vocal Files

for root, dirs, files in os.walk("vocals/mdx_extra"):
    if not files:
        continue
    prefix = os.path.basename(root)
    for f in files:
        os.rename(os.path.join(root, f), os.path.join(root, "{}_{}".format(prefix, f)))

vocals = [y for x in os.walk("vocals/mdx_extra") for y in glob(os.path.join(x[0], '*vocals.wav'))]

for f in vocals:
  shutil.move(f, "vocals")

others = [y for x in os.walk("vocals/mdx_extra") for y in glob(os.path.join(x[0], '*.wav'))]

os.mkdir("others")
for f in others:
  shutil.move(f, "others")

shutil.rmtree("vocals/mdx_extra/")

# Remove and Split on Silence --------

vocals = [y for x in os.walk("vocals") for y in glob(os.path.join(x[0], '*.wav'))]

prefixes = []
for f in vocals:
  os.system("sox '" + f + "' '" + f + "' silence 1 0.1 1% 1 0.1 1% : newfile : restart")
  os.remove(f)
  prefixes.append(os.path.basename(f)[:-4])

for prefix in prefixes:
  i = 1
  vocals = sorted([y for x in os.walk("vocals") for y in glob(os.path.join(x[0], prefix + "*"))])
  sequence = AudioSegment.from_file(vocals[0])[0:0]
  for segment in vocals:
    chunk = AudioSegment.from_file(segment)
    os.remove(segment)
    sequence += AudioSegment.silent(duration=500) # add silent frame before/in-between
    sequence += chunk
    buffer = "00"
    if i >= 10:
      buffer = "0"
    if i >= 100:
      buffer = ""
    if sequence.duration_seconds > 20:
        seq1 = sequence[0:(sequence.duration_seconds*500)]
        seq2 = sequence[(sequence.duration_seconds*500):(sequence.duration_seconds*1000)]
        seq1 += AudioSegment.silent(duration=500) # add silent frame after
        seq2 += AudioSegment.silent(duration=500) # add silent frame after
        seq1.export("vocals/" + prefix + buffer + str(i) + ".wav", format = "wav")
        i += 1
        buffer = "00"
        if i >= 10:
          buffer = "0"
        if i >= 100:
          buffer = ""
        seq2.export("vocals/" + prefix + buffer + str(i) + ".wav", format = "wav")
        sequence = sequence[0:0]
        i += 1
    else:
      if sequence.duration_seconds > 6:
        sequence += AudioSegment.silent(duration=500) # add silent frame after
        sequence.export("vocals/" + prefix + buffer + str(i) + ".wav", format = "wav")
        sequence = sequence[0:0]
        i += 1

vocals = [y for x in os.walk("vocals") for y in glob(os.path.join(x[0], '*.wav'))]
for f in vocals:
  # convert to 16K sample rate
  os.system("sox '" + f + "' -r 16000 'vocals/" + re.sub("[^a-zA-Z0-9]", "", os.path.basename(f)[:-4]) + "-clean.wav'")
  os.remove(f)
