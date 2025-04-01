library(readr)
library(dplyr)

url <- "https://yoursdearboy.github.io/git-101/data/imdb250.csv"

httr::GET(url, httr::write_disk("imdb250.csv", overwrite = T))

top <- read_csv("imdb250.csv")

top10 <- top |>
  group_by(year) |>
  filter(row_number() <= 10) |>
  ungroup()

write_csv(top10, "imdb10.csv")
