# Оглавление

- **Введение**
  В идеале какой-то питч, зачем он им может пригодиться, чтобы было интересней, но то что нужен на курсе уже норм.
  - Что такое система контроля версий (VCS)?
  - Что такое Git?
  - Установка
    То что мы давали перед занятием, кроме GitHub.
  - Настройка
  - Командная строка
- **Основы**
  - Создание репозитория (проекта)
    Показать, что это просто папка, в которой есть папка `.git` и в ней работают команды `git`.
    `git init` `git status`
  - Клонирование репозитория
    Частый способ начала работы над проектом. Хотя, может это будет в разделе про GitHub.
    `git clone`
  - Запись изменений
    Сделать пару коммитов, чтобы почувствовали, что это.
    Объяснить понятия рабочей области (working tree), staging и commit.
    `git add` `git commit`
  - Просмотр истории
    `git log` `git diff`
- **Ветви**
  - Создание ветвей
    Сделать несколько ветвей и слить их, в каждой несколько коммитов.
    Реалистичный пример, чтобы было понятно зачем это нужно.
    `git branch` `git checkout`
  - Слияние ветвей
    Показать как решать merge конфликты.
    `git merge`
  - Организация ветвей
    Описать основные подходы / шаблоны для работы с ветвями.
- **GitHub**
  - Настройка для работы с GitHub
    То что давали перед занятием - регистрация на GitHub, авторизация через токены, через ключи не будем, наверное.
  - Добавление удаленного репозитория (remote)
    В чем разница между https и ssh
    `git remote` `git fetch`
  - Работа с удаленными ветвями
    `git pull` `git push`
  - Pull Request
- **Best practices и решение частых проблем**
  - Оформление и структура репозитория
    Сказать про README, стандартные файлы
  - Файл .gitignore
  - Клиенты Git
  - Команда git amend
  - Разрешение merge conflict
  - Решение проблемы push rejection
- **Установка пакетов**
  - Зачем хранить версии пакетов
  - Установка пакетов через `renv`
  - Создание lock-файла `renv.lock`

Куда-то засунуть Rmarkdown?

## Курс на Stepik

[URL](https://stepik.org/course/123591/)

1  Основы Git

- [+] [1.1  Что такое VCS?](https://stepik.org/lesson/773925?unit=776391)
- [+] [1.2  Git](https://stepik.org/lesson/773926?unit=776392)
- [+] [1.3  Репозиторий Git](https://stepik.org/lesson/773927?unit=776393)
- [+] [1.4  Ветки (branches)](https://stepik.org/lesson/773928?unit=776394)
- [/] [1.5  Самая важная команда (git status)](https://stepik.org/lesson/773929?unit=776395)
- [+] [1.6  Сохранение изменений (git add / git commit)](https://stepik.org/lesson/773931?unit=776397)
- [+] [1.7  Создание и переключение веток (git checkout)](https://stepik.org/lesson/773932?unit=776398)

2  Продвинутый Git

- [+] [2.1  Просмотр истории коммитов (git log)](https://stepik.org/lesson/773933?unit=776399)
- [+] [2.2  Переключение между коммитами (git checkout)](https://stepik.org/lesson/773934?unit=776400)
- [+] [2.3  Слияние веток (git merge)](https://stepik.org/lesson/773935?unit=776401)
- [+] [2.4  Конфликты слияния (merge conflicts)](https://stepik.org/lesson/773936?unit=776402)
- [-] [2.5  Удаление изменений (git reset/restore)](https://stepik.org/lesson/779533?unit=782076)

3  Работа с удалёнными репозиториями

- [+] [3.1  Что такое удалённый репозиторий](https://stepik.org/lesson/773938?unit=776404)
- [+] [3.2  GitHub](https://stepik.org/lesson/773939?unit=776405)
- [-] [3.3  Bitbucket](https://stepik.org/lesson/773940?unit=776406)
- [+] [3.4  Связь удалённого репозитория с локальным](https://stepik.org/lesson/778499?unit=780983)
- [+] [3.5  Настройка аутентификации GitHub](https://stepik.org/lesson/778500?unit=780984)
- [+] [3.6  Клонирование репозитория (git clone)](https://stepik.org/lesson/773941?unit=776407)
- [+] [3.7  Сохранение изменений в удалённом репозитории (git push)](https://stepik.org/lesson/773942?unit=776408)
- [+] [3.8  Получение изменений с удалённого репозитория (git pull)](https://stepik.org/lesson/773943?unit=776409)
- [-] [3.9  Форки](https://stepik.org/lesson/773944?unit=776410)

4  Best practices

- [+] [4.1  Принципы организации веток](https://stepik.org/lesson/773945?unit=776411)
- [+] [4.2  Pull-requests](https://stepik.org/lesson/773946?unit=776412)
- [+] [4.3  README.md](https://stepik.org/lesson/779029?unit=781553)
- [+] [4.4   gitignore](https://stepik.org/lesson/779907?unit=782481)
- [-] [4.5  Полезные ссылки](https://stepik.org/lesson/795808?unit=798577)

5  Типовые примеры

- [ ] [5.1  Как сдать ДЗ | Биологи Python](https://stepik.org/lesson/773947?unit=776413)
- [ ] [5.2  Как сдать ДЗ | Биостати](https://stepik.org/lesson/795784?unit=798554)

## Git Book

[URL](https://git-scm.com/book/en/v2)

Getting Started

- [+] 1.1 About Version Control
- [-] 1.2 A Short History of Git
- [+] 1.3 What is Git?
- [+] 1.4 The Command Line
- [+] 1.5 Installing Git
- [+] 1.6 First-Time Git Setup
- [-] 1.7 Getting Help
- [-] 1.8 Summary

Git Basics

- [+] 2.1 Getting a Git Repository
- [+] 2.2 Recording Changes to the Repository
- [+] 2.3 Viewing the Commit History
- [-] 2.4 Undoing Things
- [+] 2.5 Working with Remotes
- [-] 2.6 Tagging
- [-] 2.7 Git Aliases
- [-] 2.8 Summary

Git Branching

- [?] 3.1 Branches in a Nutshell
- [+] 3.2 Basic Branching and Merging
- [?] 3.3 Branch Management
- [+] 3.4 Branching Workflows
- [+] 3.5 Remote Branches
- [?] 3.6 Rebasing
- [-] 3.7 Summary

GitHub

- [+] 6.1 Account Setup and Configuration
- [-] 6.2 Contributing to a Project
- [-] 6.3 Maintaining a Project
- [-] 6.4 Managing an organization
- [-] 6.5 Scripting GitHub
- [-] 6.6 Summary

## Happy Git with R

[URL](https://happygitwithr.com)

Тут структура: git, github, куча команд, workflow. Потому что это для workshop'а.

- [-] [Let’s Git started](https://happygitwithr.com/)
- [+] [1 Why Git? Why GitHub?](https://happygitwithr.com/big-picture)
- [-] [2 Contributors](https://happygitwithr.com/contrib)
- [-] [3 Workshops](https://happygitwithr.com/workshops)
- Installation
  - [Half the battle](https://happygitwithr.com/install-intro)
  - [+] [4 Register a GitHub account](https://happygitwithr.com/github-acct)
  - [-] [5 Install or upgrade R and RStudio](https://happygitwithr.com/install-r-rstudio)
  - [+] [6 Install Git](https://happygitwithr.com/install-git)
  - [+] [7 Introduce yourself to Git](https://happygitwithr.com/hello-git)
  - [+] [8 Install a Git client](https://happygitwithr.com/git-client)
- Connect Git, GitHub, RStudio
  - [Can you hear me now?](https://happygitwithr.com/connect-intro)
  - [+] [9 Personal access token for HTTPS](https://happygitwithr.com/https-pat)
  - [+] [10 Set up keys for SSH](https://happygitwithr.com/ssh-keys)
  - [+] [11 Connect to GitHub](https://happygitwithr.com/push-pull-github)
  - [+] [12 Connect RStudio to Git and GitHub](https://happygitwithr.com/rstudio-git-github)
  - [+] [13 Detect Git from RStudio](https://happygitwithr.com/rstudio-see-git)
  - [+] [14 RStudio, Git, GitHub Hell](https://happygitwithr.com/troubleshooting)
- Early GitHub Wins
  - [Get started with GitHub](https://happygitwithr.com/usage-intro)
  - [-] [15 New project, GitHub first](https://happygitwithr.com/new-github-first)
  - [-] [16 Existing project, GitHub first](https://happygitwithr.com/existing-github-first)
  - [+] [17 Existing project, GitHub last](https://happygitwithr.com/existing-github-last)
  - [?] [18 Test drive R Markdown](https://happygitwithr.com/rmd-test-drive)
  - [-] [19 Render an R script](https://happygitwithr.com/r-test-drive)
- Git fundamentals
  - [Some Git basics](https://happygitwithr.com/git-intro)
  - [+] [20 Repo, commit, diff, tag](https://happygitwithr.com/git-basics)
  - [+] [21 Git commands](https://happygitwithr.com/git-commands)
  - [+] [22 Branches](https://happygitwithr.com/git-branches)
  - [+] [23 Remotes](https://happygitwithr.com/git-remotes)
  - [-] [24 Refs](https://happygitwithr.com/git-refs)
- Remote setups
  - [Git remote setups](https://happygitwithr.com/remote-scenarios-intro)
  - [?] [25 Common remote setups](https://happygitwithr.com/common-remote-setups)
  - [?] [26 Equivocal remote setups](https://happygitwithr.com/equivocal)
- Daily Workflows
  - [Useful Git patterns for real life](https://happygitwithr.com/workflows-intro)
  - [+] [27 The Repeated Amend](https://happygitwithr.com/repeated-amend)
  - [+] [28 Dealing with push rejection](https://happygitwithr.com/push-rejected)
  - [?] [29 Pull, but you have local work](https://happygitwithr.com/pull-tricky)
  - [-] [30 Time travel: See the past](https://happygitwithr.com/time-travel-see-past)
  - [?] [31 Fork and clone](https://happygitwithr.com/fork-and-clone)
  - [-] [32 Get upstream changes for a fork](https://happygitwithr.com/upstream-changes)
  - [-] [33 Explore and extend a pull request](https://happygitwithr.com/pr-extend)
  - [-] [34 Make a GitHub repo browsable](https://happygitwithr.com/workflows-browsability)
- Activity prompts
  - [+] [35 Clone a repo](https://happygitwithr.com/clone)
  - [-] [36 Create a bingo card](https://happygitwithr.com/bingo)
  - [+] [37 Burn it all down](https://happygitwithr.com/burn)
  - [-] [38 Resetting](https://happygitwithr.com/reset)
  - [-] [39 Search GitHub](https://happygitwithr.com/search)
- Notes
  - [Notes](https://happygitwithr.com/notes-intro)
  - [-] [40 Run a course with GitHub](https://happygitwithr.com/classroom-overview)
  - [-] [41 Ideas for content](https://happygitwithr.com/ideas-for-content)
  - [-] [42 Bookdown cheat sheet](https://happygitwithr.com/bookdown-cheat-sheet)
- Appendix
  - [+] [A The shell](https://happygitwithr.com/shell)
  - [-] [B Comic relief](https://happygitwithr.com/comic-relief)
  - [-] [C Resources](https://happygitwithr.com/resources)
  - [-] [D References](https://happygitwithr.com/references)
