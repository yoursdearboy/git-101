---
title: "Подготовка к работе с Git и GitHub"
output:
  html_document:
    toc: true
    toc_float: true
---

# Проверьте наличие Git

Откройте Rstudio.
В верхнем меню выберите **Tools → Terminal → New Terminal**.
В терминале введите команду `git` и нажмите Enter.
Если вы видите результат как на скриншоте ниже, то Git установлен,
иначе нужно его установить - см. инструкцию ниже.

![](./img/git.png)

# Установите Git {.tabset .tabset-pills}

## Windows

Загрузите инсталлятор по ссылке [git-scm.com/downloads/win](https://git-scm.com/downloads/win)

Во время установки можно оставить опции выбранные по умолчанию.

## Mac OS

**Вариант 1.** В терминале введите:

```sh
xcode-select --install
```

В появившемся окне нажмите кнопку **Install**.

**Вариант 2.** Если у вас установлен Homebrew, в терминале введите:

```sh
brew install git
```

**Вариант 3.** Установите при помощи **Binary installer** с сайта [git-scm.com/downloads/mac](https://git-scm.com/downloads/mac)

## Linux

Для Ubuntu или Debian:

```sh
sudo apt-get install git
```

Для других дистрибутивов см. [git-scm.com/downloads/linux](https://git-scm.com/downloads/linux)
(не забудьте запустить команду с правами администратора, т.е. через `sudo` как в примере выше).

# Настройте Git

В терминале выполните следующие команды заменив на свое имя и email, указанный при регистрации на GitHub.

```sh
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

# Создайте токен (пароль) для GitHub

Для работы с GitHub вам нужно создать так называемый **Personal Access Token** -
отдельный многоразовый пароль.

Для этого перейдите по ссылке [github.com/settings/tokens](https://github.com/settings/tokens),
авторизуйтесь и нажмите **Generate new token**, в выпадающем списке выберите **classic**.

На новой странице введите название токена, например Demo.
Отметьте следующие права `repo`, `workflow`, `user`
и нажмите зеленую кнопку **Generate token** в конце страницы.

Не забудьте скопировать и сохранить ваш токен - он выглядит как строка вида

`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

После того как вы закроете страницу посмотреть созданный токен невозможно.
Храните его в надежном месте как пароль.

![](img/github-1.png){style="border: 1px solid #ccc; border-radius-top: 3px;"}
![](img/github-2.png){style="border: 1px solid #ccc; border-top: none; border-bottom: none;"}
![](img/github-3.png){style="border: 1px solid #ccc; border-radius-bottom: 3px"}

