---
title: "Makefile"
output: html_document
---

<style>
body {
    font-size: 12pt;
}
h1 {
    font-size: 20pt;
}
h2 {
    font-size: 16pt;
}
</style>

```sh
FILES=$(pwd)
ASSETS=$(pwd)/assets
ROOT=/tmp/practice
REMOTE=https://github.com/yoursdearboy/automation_homework.git
GITHUB=https://github.com/yoursdearboy/automation_homework

USER1=$ROOT/user1
USER2=$ROOT/user2
USER3=$ROOT/user3
USER4=$ROOT/user4
```

# Сетап

```sh
rm -fr $ROOT
mkdir -p $ROOT
gh repo delete $GITHUB
```

# Полезные функции

**Периодически все синкаются, для практики, в том числе координатор.**

```sh
everybody_pull() {
    cd $USER1 && git checkout main && git pull
    cd $USER2 && git checkout main && git pull
    cd $USER3 && git checkout main && git pull
    cd $USER4 && git checkout main && git pull
}
```

# 0. Перед занятием

Ева и Оля говорят про домашку, что она совместная и на гитхабе.
Перерыв 40 минут.

Показываем список команд в Google таблице, где указан юзернейм гитхаб и телеграм.
Кто сможет участвовать — ставят плюсики.
Перераспределяем команды, чтобы было 4 или хотя бы 3 человека.
Они создают чатики в телеграм и добавляют в таблицу ссылку на чат.
Заходим с Димой в чат.
Если нужна будет помощь, они тэгают меня и Диму, а еще в идеале прикладывают сообщение / скриншот ошибки.

1. Приветствие.
2. Сказать, что мы сейчас засетапим проект и репозиторий для совместного выполнения домашки, который будет являться решением.
   Сказать, что это упрощенная версия для тренировки совместной работы над домашкой и будущим проектами.
3. Презентация --- рефрешер и бест практисес.
4. Перерыв 5-10 минут, я отвечаю на вопросы, Наташа раскидывает по комнатам.
5. Практика.

# 1. Инициализируем проект

## 1.1 Создаем проект

**👮‍♂️ КООРДИНАТОР**

```sh
unzip $ASSETS/project.zip -d $ROOT
```

## 1.2. Коммитим проект

**👮‍♂️ КООРДИНАТОР**

```sh
cd $USER1
git add .
git commit -m "Создали проект R"
```

## 1.3. Создаем ПРИВАТНЫЙ репозиторий

**👮‍♂️ КООРДИНАТОР**

```sh
cd $USER1
gh repo create --private $GITHUB
```

Пушим туда сделанный коммит.

```sh
cd $USER1
git remote add origin $REMOTE
git branch -M main
git push -u --force origin main
```

## 1.4. Клонируем репозиторий

**👮‍♂️ КООРДИНАТОР**

Добавляем участников в репу.
Я добавлю Диму `Dmitrii-Belousov`.
Они добавляют и Диму и меня `yoursdearboy`.

<!-- TODO: Или сначала добавляем, а потом пушим? -->

Обратить внимание координаторов на то, чтобы инвайты были приняты.

**👷‍♂️ УЧАСТНИКИ**

Клонируем.

Показываю как клонировать.

```sh
git clone $REMOTE $USER2
git clone $REMOTE $USER3
git clone $REMOTE $USER4
```

# 2. Добавляем данные и шаблон

**👮‍♂️ КООРДИНАТОР**

Файлы берем с гугл диска.
Делаем push, чтобы пока ведущий импортирует данные,
у остальных было время сделать pull.

```sh
cd $USER1
mkdir -p data/raw
cp $ASSETS/data/raw/* data/raw/
cp $ASSETS/homework_notebook.Rmd homework_notebook.Rmd
git add .
git commit -m "Загрузили данные и шаблон"
git push
```

**👷‍♂️ УЧАСТНИКИ**

Далем pull.
После каждого этапа мы будем возвращаться к ветке `main` и делать pull.

```sh
everybody_pull
```

# 3. Подписываем задания для импорта

**👷‍♂️ УЧАСТНИКИ** создают ветку со своим именем, подписывают в чанке задание, делают пуш и PR.

**👮‍♂️ КООРДИНАТОР** их сливает.
Проговорить, что надо смотреть изменения на вкладке Files.

**👮‍♂️👷‍♂️ ВСЕ** делают pull.

```sh
cd $USER2
git checkout -b user2
git apply $FILES/06u2.patch
git add .
git commit -m "Подписал задания"
git push -u --force origin user2
gh pr create --title "Подписал задания" --body ""
```

```sh
cd $USER3
git checkout -b user3
git apply $FILES/06u3.patch
git add .
git commit -m "Подписал задания"
git push -u --force origin user3
gh pr create --title "Подписал задания" --body ""
```

```sh
cd $USER4
git checkout -b user4
git apply $FILES/06u4.patch
git add .
git commit -m "Подписал задания"
git push -u --force origin user4
gh pr create --title "Подписал задания" --body ""
```

```sh
cd $USER1
gh pr merge --merge user2
gh pr merge --merge user3
gh pr merge --merge user4
```

**👮‍♂️👷‍♂️ ВСЕ** делают pull.

```sh
everybody_pull
```

# 4. Каждый делает по заданию — импорт (кроме ведущего)

Проговорить, что надо не только смотреть изменения, но и делать чекаут.

<!-- TODO: где-то Дима должен будет сделать push, а я checkout, чтобы показать как это работает -->
<!-- TODO: еще бы координатор повзаимодействовал с исполнителем -->

```sh
cd $USER2
git checkout -b dm
git apply $FILES/07u2.patch
git add .
git commit -m "Импортировал демографические данные"
git push -u --force origin dm
gh pr create --title "Импортировал демографические данные" --body ""
```

```sh
cd $USER3
git checkout -b vs
git apply $FILES/07u3.patch
git add .
git commit -m "Импортировал vs"
git push -u --force origin vs
gh pr create --title "Импортировал vs" --body ""
```

```sh
cd $USER4
git checkout -b lb
git apply $FILES/07u4.patch
git add .
git commit -m "Импортировал лабораторные измерения lb"
git push -u --force origin lb
gh pr create --title "Импортировал лабораторные измерения lb" --body ""
```

```sh
cd $USER1
gh pr merge --merge dm
gh pr merge --merge vs
gh pr merge --merge lb
```

```sh
everybody_pull
```

# 5. Ведущий делает join

```sh
cd $USER1
git checkout -b join
git apply $FILES/08u1.patch
git add .
git commit -m "Объединил данные"
git push -u --force origin join
gh pr create --title "Объединил данные" --body ""
gh pr merge --merge join
```

```sh
everybody_pull
```

# 6. Все делают боксплоты (кроме ведущего)

<!-- TODO: -->
<!-- Ведущий резолвит конфликты? -->
<!-- Или каждый участник резолвит? -->

<!-- TODO: хорошо бы на экране показать как резолвить. -->

```sh
cd $USER2
git checkout -b boxplot-temp-sex
git apply $FILES/09u2.patch
git add .
git commit -m "Построил боксплот температуры тела от пола"
git push -u --force origin boxplot-temp-sex
gh pr create --title "Построил боксплот температуры тела от пола" --body ""
```

```sh
cd $USER3
git checkout -b boxplot-temp-actarm
git apply $FILES/09u3.patch
git add .
git commit -m "Построил боксплот температуры тела от группы"
git push -u --force origin boxplot-temp-actarm
gh pr create --title "Построил боксплот температуры тела от группы" --body ""
```

```sh
cd $USER4
git checkout -b boxplot-wbc-actarm
git apply $FILES/09u4.patch
git add .
git commit -m "Построил боксплот кол-ва лейкоцитов от группы"
git push -u --force origin boxplot-wbc-actarm
gh pr create --title "Построил боксплот кол-ва лейкоцитов от группы" --body ""
```

<!-- TODO: у гитхаба инструкция работает не на всех версиях Git -->
<!-- на старых нужен fetch -->

```sh
cd $USER1
git fetch
gh pr merge --merge boxplot-wbc-actarm
# резолвим boxplot-temp-actarm
git checkout main
git pull origin main
git checkout boxplot-temp-actarm
git merge main
git apply $FILES/09u1-01.patch
git add .
git commit -m "Resolved conflicts"
git push
gh pr merge --merge boxplot-temp-actarm
# резолвим второй PR
git checkout main
git pull origin main
git checkout boxplot-temp-sex
git merge main || true
git apply $FILES/09u1-02.patch
git add .
git commit -m "Resolved conflicts"
git push
gh pr merge --merge boxplot-temp-sex
```

```sh
everybody_pull
```
