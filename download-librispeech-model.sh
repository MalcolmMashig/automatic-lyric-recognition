# download-librispeech-model.sh

mkdir librispeech-tools
cd librispeech-tools
wget http://kaldi-asr.org/models/13/0013_librispeech_v1_chain.tar.gz
wget http://kaldi-asr.org/models/13/0013_librispeech_v1_extractor.tar.gz
wget http://kaldi-asr.org/models/13/0013_librispeech_v1_lm.tar.gz
cd ..
docker cp $base_dir/librispeech-tools/. $docker_cid:opt/kaldi/egs/wsj/s5/librispeech-tools