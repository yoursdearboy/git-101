.ONESHELL:
.SHELLFLAGS += -e

PWD := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ASSETS := $(PWD)/assets
ROOT := /tmp/practice
REMOTE := https://github.com/yoursdearboy/automation_homework.git
GITHUB := https://github.com/yoursdearboy/automation_homework

USER1 := $(ROOT)/user1
USER2 := $(ROOT)/user2
USER3 := $(ROOT)/user3
USER4 := $(ROOT)/user4

# Служебные
clean:
	rm -fr $(ROOT)
	gh repo delete --yes $(GITHUB) || true

prompt:
	@echo -n "Have you merged PRs? [y/N] " && read ans && [ $${ans:-N} = y ]

# Все синкаются, для практики, в том числе координатор
everybody_pull:
	cd $(USER1) && git checkout main && git pull
	cd $(USER2) && git checkout main && git pull
	cd $(USER3) && git checkout main && git pull
	cd $(USER4) && git checkout main && git pull

step0:
	mkdir -p $(ROOT)

# 1. Создаем проект
step1_user1: step0
	unzip assets/project.zip -d $(ROOT)

step1: step0 step1_user1

# 2. Коммитим проект
step2_user1: step1
	cd $(USER1)
	git add .
	git commit -m "Создали проект R"

step2: step1 step2_user1

# 3. Создаем ПРИВАТНЫЙ репозиторий
step3_user1: step2
	cd $(USER1)
	gh repo create --private $(GITHUB)
	git remote add origin $(REMOTE)
	git branch -M main
	git push -u --force origin main

step3: step2 step3_user1

# 4. Все получают проект

# Добавляем участников в репу, в том числе меня
# Обратить внимание координаторов на то, чтобы инвайты были приняты
step4_user1:

# Все клонируют (кроме ведущего)
step4_user234: step3
	git clone $(REMOTE) $(USER2)
	git clone $(REMOTE) $(USER3)
	git clone $(REMOTE) $(USER4)

step4: step3 step4_user1 step4_user234

# 5. Добавляем данные и шаблон

# Файлы берем с гугл диска.
# Делаем push, чтобы пока ведущий импортирует данные,
# у остальных было время сделать pull.
step5_user1:
	cd $(USER1)
	mkdir -p data/raw
	cp $(ASSETS)/data/raw/* data/raw/
	cp $(ASSETS)/homework_notebook.Rmd homework_notebook.Rmd
	git add .
	git commit -m "Загрузили данные и шаблон"
	git push

step5: step4 step5_user1 everybody_pull

# 6. Все подписывают задания — импорт (кроме ведущего)
# Проговорить, что надо смотреть изменения на вкладке Files.

step6_user2:
	cd $(USER2)
	git checkout -b user2
	git apply $(PWD)/06u2.patch
	git add .
	git commit -m "Подписал задания"
	git push -u --force origin user2
	gh pr create --title "Подписал задания" --body ""

step6_user3:
	cd $(USER3)
	git checkout -b user3
	git apply $(PWD)/06u3.patch
	git add .
	git commit -m "Подписал задания"
	git push -u --force origin user3
	gh pr create --title "Подписал задания" --body ""

step6_user4:
	cd $(USER4)
	git checkout -b user4
	git apply $(PWD)/06u4.patch
	git add .
	git commit -m "Подписал задания"
	git push -u --force origin user4
	gh pr create --title "Подписал задания" --body ""

step6_user1:
	cd $(USER1)
	gh pr merge --merge user2
	gh pr merge --merge user3
	gh pr merge --merge user4

step6: step5 step6_user2 step6_user3 step6_user4 step6_user1 everybody_pull

# 7. Каждый делает по заданию — импорт (кроме ведущего)
# Проговорить, что надо не только смотреть изменения, но и делать чекаут.
# TODO: где-то Дима должен будет сделать push, а я checkout, чтобы показать как это работает
# TODO: еще бы координатор повзаимодействовал с исполнителем

step7_user2:
	cd $(USER2)
	git checkout -b dm
	git apply $(PWD)/07u2.patch
	git add .
	git commit -m "Импортировал демографические данные"
	git push -u --force origin dm
	gh pr create --title "Импортировал демографические данные" --body ""

step7_user3:
	cd $(USER3)
	git checkout -b vs
	git apply $(PWD)/07u3.patch
	git add .
	git commit -m "Импортировал vs"
	git push -u --force origin vs
	gh pr create --title "Импортировал vs" --body ""

step7_user4:
	cd $(USER4)
	git checkout -b lb
	git apply $(PWD)/07u4.patch
	git add .
	git commit -m "Импортировал лабораторные измерения lb"
	git push -u --force origin lb
	gh pr create --title "Импортировал лабораторные измерения lb" --body ""

step7_user1:
	cd $(USER1)
	gh pr merge --merge dm
	gh pr merge --merge vs
	gh pr merge --merge lb

step7: step6 step7_user2 step7_user3 step7_user4 step7_user1 everybody_pull

# 8. Ведущий делает join

step8_user1:
	cd $(USER1)
	git checkout -b join
	git apply $(PWD)/08u1.patch
	git add .
	git commit -m "Объединил данные"
	git push -u --force origin join
	gh pr create --title "Объединил данные" --body ""
	gh pr merge --merge join

step8: step7 step8_user1 everybody_pull

# 9. Все делают боксплоты (кроме ведущего)
# TODO:
# Ведущий резолвит конфликты?
# Или каждый участник резолвит?
# TODO: хорошо бы на экране показать как резолвить.

step9_user2:
	cd $(USER2)
	git checkout -b boxplot-temp-sex
	git apply $(PWD)/09u2.patch
	git add .
	git commit -m "Построил боксплот температуры тела от пола"
	git push -u --force origin boxplot-temp-sex
	gh pr create --title "Построил боксплот температуры тела от пола" --body ""

step9_user3:
	cd $(USER3)
	git checkout -b boxplot-temp-actarm
	git apply $(PWD)/09u3.patch
	git add .
	git commit -m "Построил боксплот температуры тела от группы"
	git push -u --force origin boxplot-temp-actarm
	gh pr create --title "Построил боксплот температуры тела от группы" --body ""

step9_user4:
	cd $(USER4)
	git checkout -b boxplot-wbc-actarm
	git apply $(PWD)/09u4.patch
	git add .
	git commit -m "Построил боксплот кол-ва лейкоцитов от группы"
	git push -u --force origin boxplot-wbc-actarm
	gh pr create --title "Построил боксплот кол-ва лейкоцитов от группы" --body ""

# TODO: у гитхаба инструкция работает не на всех версиях Git
# на старых нужен fetch
step9_user1:
	cd $(USER1)
	git fetch
	gh pr merge --merge boxplot-wbc-actarm
# резолвим boxplot-temp-actarm
	git checkout main
	git pull origin main
	git checkout boxplot-temp-actarm
	git merge main || true
	git apply $(PWD)/09u1-01.patch
	git add .
	git commit -m "Resolved conflicts"
	git push
	gh pr merge --merge boxplot-temp-actarm
# резолвим второй PR
	git checkout main
	git pull origin main
	git checkout boxplot-temp-sex
	git merge main || true
	git apply $(PWD)/09u1-02.patch
	git add .
	git commit -m "Resolved conflicts"
	git push
	gh pr merge --merge boxplot-temp-sex

step9: step9_user2 step9_user3 step9_user4 step9_user1 everybody_pull
