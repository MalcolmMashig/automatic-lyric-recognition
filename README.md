# Automatic Lyric Recognition
### Transcribe Lyrics with the LibriSpeech ASR Model

We are guided by the steps outlined in https://seongminpark.com/blog/20201222a/ which follows the WSJ recipe.

Once you have Docker Desktop downloaded and running, enter the following terminal commands:

`git clone https://github.com/MalcolmMashig/automatic-lyric-recognition.git`

`cd automatic-lyric-recognition`

##### 1. Make sure that all audio files to transcribe are located in `audio_dir`:

`export base_dir=pwd`

`export audio_dir=$base_dir/audio`


##### 2. Prepare the Audio and Kaldi Docker container:

`source prep-docker.sh`

`source download-librispeech-model.sh`

`source prep-audio.sh`


##### 3. Enter the container:

`docker exec -it $docker_cid bash`


##### 4. Run the decoding process:

`source docker-delivery/transcribe.sh`


##### 5. Press {CTRL p} then {CTRL q} to exit the container.


##### 6. Copy over the transcriptions from the container to your local machine:

`decoded_path=opt/kaldi/egs/wsj/s5/exp/chain_cleaned/tdnn_1d_sp/decode_convert_me_tgsmall/score_20/convert_me.ctm`

`docker cp $docker_cid:$decoded_path $base_dir/transcriptions.ctm`

