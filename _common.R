# example R options set globally
options(width = 60)

if (!requireNamespace("downlit", quietly = TRUE)) {
  stop("Для сборки bs4_book установите downlit через renv::restore()")
}

# example chunk options set globally
knitr::opts_chunk$set(
  comment = "#>",
  collapse = TRUE
  )
