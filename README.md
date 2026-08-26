# Основы Git в Positron

Курс продолжает проект `r-course` из соседнего репозитория: студент фиксирует накопленные файлы без преобразований, а новую работу выполняет в `paper.qmd`.

Источники книги остаются в Bookdown. Собрать сайт:

```sh
make build
```

Запустить проверки генератора и учебного текста:

```sh
make test
```

## Генератор учебного проекта

Стартовое дерево в `course-project/starter/` собрано по заданиям R-курса. В нём намеренно сохранены накопленные `.R`, `.qmd`, данные и результаты. Генератор копирует это дерево без переименования и проверяет размер и SHA-256 каждого файла по `course-project/starter-manifest.json`.

```sh
python3 bin/create_course_project.py /tmp/r-course-student --state starter
```

Локальные состояния:

```text
starter baseline paper histogram boxplot-branch dirty-main conflict merged
```

Например, воспроизвести незавершённый конфликт слияния:

```sh
python3 bin/create_course_project.py /tmp/r-course-conflict --state conflict
```

GitHub-состояния используют установленный [GitHub CLI](https://cli.github.com/) и создают настоящий репозиторий:

```sh
python3 bin/create_course_project.py /tmp/r-course-github \
  --state github-pr \
  --repo OWNER/REPOSITORY \
  --visibility private
```

Доступны `github-published`, `github-pr`, `github-merged` и `github-webhook`. Для webhook добавьте `--webhook-url`; секрет можно передать через `--webhook-secret`.

Если `gh auth status` не проходит, генератор запускает `gh auth login --web` и ждёт подтверждения в браузере. Он отказывается продолжать, если целевая папка или удалённый репозиторий уже существуют, и никогда не изменяет соседний репозиторий `r-course`.
