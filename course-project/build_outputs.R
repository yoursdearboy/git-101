data <- read.csv("course-project/updates/penguins.csv")
x <- data$bill_len
g <- data$sex

png("course-project/outputs/penguins-hist.png")
hist(x, breaks = seq(30, 60, 2))
dev.off()

png("course-project/outputs/penguins-boxplot.png")
boxplot(x)
dev.off()

png("course-project/outputs/penguins-boxplot-labelled.png")
boxplot(x, ylab = "Bill length, mm")
dev.off()

png("course-project/outputs/penguins-boxplot-by-sex.png")
boxplot(x ~ g, xlab = "Sex", ylab = "Bill length, mm")
dev.off()
