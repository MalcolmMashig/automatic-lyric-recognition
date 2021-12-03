# download-audio.R

# install.packages("spotifyr")
library(spotifyr)
library(tidyverse)

plist <- get_my_playlists(50) %>% 
  filter(name == "ALR")
dir.create("audio")
folder <- "/Users/malcolm_mashig/box-sync/IMPORTANT/FSR/automatic-lyric-recognition/audio"
filenames <- list.files(folder)

tracks <- NULL
i <- 0
for (i in seq(0, plist %>% pull(tracks.total), 50)) {
  tracks <- tracks %>% 
    bind_rows(
      get_playlist_tracks(
        plist %>% pull(id),
        limit = 50,
        offset = i
      )
    )
}

tracks <- tracks %>% 
  as_tibble() %>% 
  mutate(
    added_at = lubridate::ymd(substr(added_at, 1, 10))
  ) %>% 
  arrange(desc(added_at)) %>% 
  select(-added_at) %>% 
  distinct(track.id, .keep_all = TRUE)

artists <- NULL
for (i in 1:nrow(tracks)) {
  artist <- tracks$track.artists[[i]]$name[1]
  artists <- artists %>% c(artist)
}

command <- NULL
for (i in 1:nrow(tracks)) {
  name <- tracks$track.name[i] %>% 
    str_remove_all("'")
  artist <- artists[i] %>% 
    str_remove_all("'")
  name_regex <- "["
  for(j in 1:nchar(name)) {
    letter <- substr(name, j, j)
    if (letter %>% str_detect("[a-zA-Z]")) {
      name_regex <- name_regex %>% str_c(
        letter %>% str_to_lower(), letter %>% str_to_upper(), "]["
      )
    } else {
      name_regex <- name_regex %>% str_c(letter, "][")
    }
  }
  name_regex <- substr(name_regex, 1, nchar(name_regex) - 1)
  artist_regex <- "["
  for(j in 1:nchar(artist)) {
    letter <- substr(artist, j, j)
    if (letter %>% str_detect("[a-zA-Z]")) {
      artist_regex <- artist_regex %>% str_c(
        letter %>% str_to_lower(), letter %>% str_to_upper(), "]["
      )
    } else {
      artist_regex <- artist_regex %>% str_c(letter, "][")
    }
  }
  artist_regex <- substr(artist_regex, 1, nchar(artist_regex) - 1)
  filename <- str_c(artist %>% str_replace_all("/", "_"), "|||", name %>% str_replace_all("/", "_"), ".wav")
  if (!((filename %>% str_to_lower()) %in% (filenames %>% str_to_lower()))) {
    command <- str_c(
      "youtube-dl --external-downloader aria2c --external-downloader-args '-c -j 3 -x 3 -s 3 -k 1M' -f 'bestaudio[filesize<5M]' --max-downloads 1 --max-filesize 5m --no-playlist --extract-audio --audio-format 'wav' ",
      "-o '", folder, "/",
      artist %>% str_replace_all("/", "_"), "|||", name %>% str_replace_all("/", "_"), 
      ".$(ext)s' 'ytsearch1:",
      name, " ", artist, 
      "'"
    )
    system(command)
  }
}
