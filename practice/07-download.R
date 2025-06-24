library(readr)
library(dplyr)

url <- "https://yoursdearboy.github.io/git-101/data/imdb250.csv"

httr::GET(url, httr::write_disk("imdb.csv", overwrite = T))

top <- read_csv("imdb.csv")

top100 <- top |>
  group_by(year) |>
  filter(row_number() <= 100) |>
  ungroup()

write_csv(top100, "imdb.csv")
