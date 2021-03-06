# prep-audio.sh

# Prepares all audio files in `audio_dir` and copies them to Docker container

python3 isolate-vocals.py

python3 normalize-test-data.py

mv vocals docker-delivery/vocals

Rscript generate_wavscp_utt2spk.R

docker cp $base_dir/docker-delivery/. $docker_cid:opt/kaldi/egs/wsj/s5/docker-delivery