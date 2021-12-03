
dir.create("docker-delivery/data/convert_me", recursive = TRUE)
vocals <- list.files(file.path("docker-delivery", "vocals"))
writeLines(
  paste0(substr(vocals, 1, nchar(vocals) - 4), 
         " /opt/kaldi/egs/wsj/s5/docker-delivery/vocals/", vocals), 
  "docker-delivery/data/convert_me/wav.scp"
)
writeLines(
  paste0(substr(vocals, 1, nchar(vocals) - 4), " ", 
         substr(vocals, 1, nchar(vocals) - 4)),
  "docker-delivery/data/convert_me/utt2spk"
)
