library(readr)
library(dplyr)

url <- "https://yoursdearboy.github.io/git-101/data/billboard100.csv"

httr::GET(url, httr::write_disk("billboard.csv", overwrite = T))

top <- read_csv("billboard.csv")

top10 <- top |>
  group_by(Date) |>
  filter(row_number() <= 10) |>
  ungroup()

write_csv(top10, "billboard.csv")
