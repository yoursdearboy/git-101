# (PART) Основы {-}

# Создание репозитория (init) {#git-init}

Показать, что это просто папка, в которой есть папка `.git` и в ней работают команды `git`.

Открыли терминал. Чтобы понять где мы находимя выполним следующую команду

```sh
pwd # в моем случае /Users/kvoronin
```

Создадим и перейдем в новую папку:

```sh
mkdir hello-git
cd hello-git
```

Попробуем вызвать команду `git status`:

```sh
git status
# fatal: not a git repository (or any of the parent directories): .git
```

Действительно пусто

```sh
ls -A # не выведет ничего, потому что нет файлов
```

![](./img/02-01-git-init.png){width=200px}

Инициализируем Git:

```sh
git init
# Initialized empty Git repository in /Users/kvoronin/hello-101/.git/
```

Проверим, что появилась папка `.git`:

```sh
ls -A
# .git
```

И снова попробуем вызвать команду `git status`:

```sh
git status
# On branch main
#
# No commits yet
#
# nothing to commit (create/copy files and use "git add" to track)
```

В последней строке Git сообщает, что нет файлов и предлагает созданные / скопированные файлы отслеживать командой `git add`.
