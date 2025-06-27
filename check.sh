#!/bin/bash

GIT_URL=https://github.com/yoursdearboy/gitfun-demo.git
STEPS="\
3c065bf12650486ea49b68c048bf4e07d74f2b44 ; Шаг 1. Создание репозитория.
9502e54a4ac3801de82acaf1c7edfef928b9608e ; Шаг 2. Добавление файлов.
c5efaeaeb197acda1cb7ef8570a14944a419d8d8 ; Шаг 3. Больше файлов.
1280dbf40ffcbd4335bcdb3ce59e25dc08c0c20b ; Шаг 4. Удаление файлов."

function init() {
  git remote add check $GIT_URL >/dev/null
  git fetch -q check
}

function cleanup() {
  git remote rm check
}

function check-step() {
  # $1 - our commit
  # $2 - user commit
  git diff -b --quiet --exit-code $1 $2
}

function echo-diff() {
  # $1 - our commit
  # $2 - filter
  files=$(git diff -b --no-renames --name-only --diff-filter=$2 $1 HEAD)
  if [[ "$files" ]]; then
    echo "$3"
    while IFS= read -r file; do
      echo "   - $file"
    done <<< "$files"
  fi
}

function echo-errors() {
  # $1 - our commit
  echo
  echo-diff $1 AC "   Лишние файлы:"
  echo-diff $1 D  "   Несуществующие файлы:"
  echo-diff $1 M  "   Неверное содержимое:"
  echo-diff $1 TUXB  "   Другие ошибки:"
  echo
  echo "   Ссылка на правильный результат https://github.com/yoursdearboy/gitfun-demo/tree/$1"
}

function process-step() {
  # $1 - our commit
  # $2 - msg
  found=1
  for shanum in $(git rev-list --reverse HEAD); do
    if check-step $1 $shanum; then
      echo "✅ $2"
      found=0
      break
    fi
  done
  if [ "$found" = 1 ]; then
    echo "❌ $2"
    echo-errors $1
    exit 1
  fi
  echo
}

function main() {
  while IFS= read -r step; do
    IFS=';';
    step=($step);
    unset IFS;
    process-step ${step[0]} "${step[1]}"
  done <<< "$STEPS"
}

if [ ! -x "$(command -v git)" ]; then
  echo "❌ Git не установлен или не найден."
  echo "   Установите Git и выполните команду   git   для проверки."
  echo "   Подробнее см. https://yoursdearboy.github.io/git-101/install.html"
  exit 1
fi

if [ ! -d .git ]; then
  echo "❌ Директория .git не найдена."
  echo "   Создайте или перейдите в Git репозиторий."
  echo "   Подробнее см. https://yoursdearboy.github.io/git-101/git-init.html"
  exit 1
fi

if [[ -z $(git log 2> /dev/null) ]]; then
  echo "❌ Нет выполненных коммитов."
  echo "   Добавьте файлы согласно инструкции и повторите проверку."
  echo "   Подробнее см. https://yoursdearboy.github.io/git-101/git-commit.html"
  echo "   Ссылка на правильный результат https://github.com/yoursdearboy/gitfun-demo/tree/3c065bf12650486ea49b68c048bf4e07d74f2b44"
  exit 1
fi

# cleanup on exit
trap cleanup EXIT

# init now
init

# do the stuff
main
