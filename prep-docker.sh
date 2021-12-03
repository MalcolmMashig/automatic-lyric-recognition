# prep-docker.sh

docker run -it -d kaldiasr/kaldi:latest bash
export docker_cid=$(docker ps -q -l)