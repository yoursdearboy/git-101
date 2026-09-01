penguins <- read.csv("data/penguins.csv")
dream <- subset(penguins, island == "Dream")

gigapeng <- max(dream$flipper_len)

png("out/hist.png", width = 800, height = 600)
hist(dream$flipper_len)
dev.off()

