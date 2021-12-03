# transcribe.sh

# Called within Docker container; transcribes audio

cd egs/wsj/s5
mkdir -p data
mv docker-delivery/data/convert_me data/
mv docker-delivery/0013_librispeech_v1_chain.tar.gz 0013_librispeech_v1_chain.tar.gz
mv docker-delivery/0013_librispeech_v1_extractor.tar.gz 0013_librispeech_v1_extractor.tar.gz
mv docker-delivery/0013_librispeech_v1_lm.tar.gz 0013_librispeech_v1_lm.tar.gz
tar -xvzf 0013_librispeech_v1_chain.tar.gz
tar -xvzf 0013_librispeech_v1_extractor.tar.gz
tar -xvzf 0013_librispeech_v1_lm.tar.gz
utils/utt2spk_to_spk2utt.pl data/convert_me/utt2spk > data/convert_me/spk2utt
utils/copy_data_dir.sh data/convert_me data/convert_me_hires
export train_cmd="run.pl"
export decode_cmd="run.pl --mem 2G"
steps/make_mfcc.sh --nj 1 --mfcc-config conf/mfcc_hires.conf --cmd "$train_cmd" data/convert_me_hires
steps/compute_cmvn_stats.sh data/convert_me_hires
utils/fix_data_dir.sh data/convert_me_hires
nspk=$(wc -l <data/convert_me_hires/spk2utt)
steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj "${nspk}" data/convert_me_hires exp/nnet3_cleaned/extractor exp/nnet3_cleaned/ivectors_convert_me_hires
export dir=exp/chain_cleaned/tdnn_1d_sp
export graph_dir=$dir/graph_tgsmall
utils/mkgraph.sh --self-loop-scale 1.0 --remove-oov data/lang_test_tgsmall $dir $graph_dir
steps/nnet3/decode.sh --acwt 1.0 --post-decode-acwt 10.0 --nj 1 --cmd "$decode_cmd" --online-ivector-dir exp/nnet3_cleaned/ivectors_convert_me_hires $graph_dir data/convert_me_hires $dir/decode_convert_me_tgsmall
steps/get_ctm.sh data/convert_me exp/chain_cleaned/tdnn_1d_sp/graph_tgsmall exp/chain_cleaned/tdnn_1d_sp/decode_convert_me_tgsmall
