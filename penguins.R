library(palmerpenguins)

gentoo <- penguins[penguins$species == "Gentoo",]

write.csv(gentoo, "penguins.csv", row.names = FALSE, na = "")
