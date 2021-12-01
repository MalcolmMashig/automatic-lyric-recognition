# normalize-test-data.py

# Isolate Vocals --------

# # Customize the following options!
# mp3 = False
# model = "mdx_extra"
# extensions = ["flac"]
# in_path = 'mini-librispeech/dev-clean/1272/141231'
# out_path = 'mini-librispeech/dev-clean/1272/141231-vocals'
# 
# #@title Useful functions, don't forget to execute
# import io
# from pathlib import Path
# import select
# from shutil import rmtree
# import subprocess as sp
# import sys
# from typing import Dict, Tuple, Optional, IO
# 
# def find_files(in_path):
#     out = []
#     for file in Path(in_path).iterdir():
#         if file.suffix.lower().lstrip(".") in extensions:
#             out.append(file)
#     return out
# 
# def copy_process_streams(process: sp.Popen):
#     def raw(stream: Optional[IO[bytes]]) -> IO[bytes]:
#         assert stream is not None
#         if isinstance(stream, io.BufferedIOBase):
#             stream = stream.raw
#         return stream
# 
#     p_stdout, p_stderr = raw(process.stdout), raw(process.stderr)
#     stream_by_fd: Dict[int, Tuple[IO[bytes], io.StringIO, IO[str]]] = {
#         p_stdout.fileno(): (p_stdout, sys.stdout),
#         p_stderr.fileno(): (p_stderr, sys.stderr),
#     }
#     fds = list(stream_by_fd.keys())
# 
#     while fds:
#         # `select` syscall will wait until one of the file descriptors has content.
#         ready, _, _ = select.select(fds, [], [])
#         for fd in ready:
#             p_stream, std = stream_by_fd[fd]
#             raw_buf = p_stream.read(2 ** 16)
#             if not raw_buf:
#                 fds.remove(fd)
#                 continue
#             buf = raw_buf.decode()
#             std.write(buf)
#             std.flush()
# 
# def separate(inp=None, outp=None):
#     inp = inp or in_path
#     outp = outp or out_path
#     cmd = ["python3", "-m", "demucs.separate", "-o", str(outp), "-n", model]
#     if mp3:
#         cmd += ["--mp3", f"--mp3-bitrate={mp3_rate}"]
#     files = [str(f) for f in find_files(inp)]
#     if not files:
#         print(f"No valid audio files in {in_path}")
#         return
#     print("Going to separate the files:")
#     print('\n'.join(files))
#     print("With command: ", " ".join(cmd))
#     p = sp.Popen(cmd + files, stdout=sp.PIPE, stderr=sp.PIPE)
#     copy_process_streams(p)
#     p.wait()
#     if p.returncode != 0:
#         print("Command failed, something went wrong.")
#         
# separate()

# Remove and Split on Silence --------

import os

# quick way
os.system("sox vocals.mp3 vocals-no-silence.wav silence 1 0.1 1% 1 0.1 1% : newfile : restart")
  
import pydub
from pydub import AudioSegment
import glob

i = 0
sequence = AudioSegment.from_file("vocals.mp3")[0:0]
for segment in sorted(glob.glob("*.wav")):
  chunk = AudioSegment.from_file(segment)
  os.remove(segment)
  sequence += AudioSegment.silent(duration=500) # add silent frame before/in-between
  sequence += chunk
  if sequence.duration_seconds > 20:
      seq1 = sequence[0:(sequence.duration_seconds*500)]
      seq2 = sequence[(sequence.duration_seconds*500):(sequence.duration_seconds*1000)]
      seq1 += AudioSegment.silent(duration=500) # add silent frame after
      seq2 += AudioSegment.silent(duration=500) # add silent frame after
      seq1.export(str(i) + "vocals-clean.flac", format = "flac")
      i += 1
      seq2.export(str(i) + "vocals-clean.flac", format = "flac")
      sequence = sequence[0:0]
      i += 1
  else:
    if sequence.duration_seconds > 6:
      sequence += AudioSegment.silent(duration=500) # add silent frame after
      sequence.export(str(i) + "vocals-clean.flac", format = "flac")
      sequence = sequence[0:0]
      i += 1
    
  






