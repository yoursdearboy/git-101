# Слияние и конфликт {#merge-conflict}

Сейчас `main` и `boxplot` по-разному изменили одну строку `paper.qmd`. Объединим ветки и разрешим конфликт осознанно.

Переключитесь на `main`. Откройте палитру команд, выполните **Git: Merge Branch** и выберите `boxplot`.

Git автоматически объединит независимые изменения, но остановится на `paper.qmd`: обе ветки изменили код графика, и программа не знает, какой вариант нужен.

В Source Control файл появится в разделе **Merge Changes** с предупреждением. Это незавершённое слияние, а не повреждение проекта.

![Source Control после Git: Merge Branch: paper.qmd находится в Merge Changes, слияние ожидает решения]()

## Редактор слияний

Нажмите `paper.qmd` правой кнопкой и выберите **Open in Merge Editor**. Редактор показывает три области:

- **Incoming** — изменение из `boxplot`;
- **Current** — изменение из `main`;
- **Result** — итог, который будет записан.

В Result оставьте боксплот из Incoming и добавьте к нему подпись из Current:

```r
png("out/penguins-boxplot.png")
boxplot(x, ylab = "Bill length, mm")
dev.off()
```

Нажмите **Complete Merge**. Убедитесь, что в Result нет строк `<<<<<<<`, `=======` и `>>>>>>>`, а `paper.qmd` находится в **Staged Changes**.

![Редактор слияний Positron: Incoming содержит boxplot, Current — hist с подписью, Result — boxplot с ylab]()

Обновите `out/penguins-boxplot.png`, добавьте его в индекс и создайте коммит `Слил ветку boxplot`.

Если нужно отказаться от всего слияния, выполните **Git: Abort Merge** из палитры команд. Git вернёт проект к состоянию до попытки merge.
