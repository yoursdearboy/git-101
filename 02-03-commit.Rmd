# Запись изменений (add, commit) {#git-commit}

Термины:

- staging

*Сделать пару коммитов, чтобы почувствовали, что это.*
*Объяснить понятия рабочей области (working tree), staging и commit.*
*`git add` `git commit`*

---

Скопируйте файл `check.sh` из предыдущего шага в свою рабочую директорию.

Проверим статус:

```sh
git status
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#       check.sh
```

Untracked files означает, что это новый файл, который ранее не отслеживался.
Добавим его при помощи команды `git add` как предлагает Git.

```sh
git add check.sh
```

Проверим статус теперь:

```sh
# Changes to be committed:
#   (use "git rm --cached <file>..." to unstage)
#       new file:   check.sh
```

Супер, мы добавили файл в область staging и теперь можем зафиксировать изменения.

```sh
git commit -m "Добавили файл для проверки заданий"
```

Используем его для проверки:

```sh
```
