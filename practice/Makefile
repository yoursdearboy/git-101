.ONESHELL:
.SHELLFLAGS += -e

PWD := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ASSETS := $(PWD)/assets
ROOT := /tmp/practice
REMOTE := https://github.com/yoursdearboy/practice.git
GITHUB := https://github.com/yoursdearboy/practice

USER1 := $(ROOT)/project
USER2 := $(ROOT)/user2
USER3 := $(ROOT)/user3
USER4 := $(ROOT)/user4

clean:
	rm -fr $(ROOT)

step0:
	mkdir -p $(ROOT)

# Создаем проект
# TODO: как назвать проект? пока project, надо automatization
step1: step0
	unzip assets/01-project.zip -d $(ROOT)

# Создаем коммит
step2: step1
	cd $(USER1)
	git add .
	git commit -m "Создали проект R"

# Пуш
step3: step2
	cd $(USER1)
	git remote add origin $(REMOTE)
	git branch -M main
	git push -u --force origin main

# Все клонируют (кроме ведущего)
step4: step3
	git clone $(REMOTE) $(USER2)
	git clone $(REMOTE) $(USER3)
	git clone $(REMOTE) $(USER4)

# Добавляем данные
# Делаем push, чтобы пока ведущий импортирует данные,
# у остальных было время сделать pull.
# TODO: Учесть практику с проекта и скопировать в data/___
step5: step4
	cd $(USER1)
	mkdir -p data/raw
	cp $(ASSETS)/data/raw/data.csv data/raw/
	git add .
	git commit -m "Загрузили данные"
	git push
	cd $(USER2) && git pull
	cd $(USER3) && git pull
	cd $(USER4) && git pull

# Импортируем данные
# Обратить внимание на пути при написании кода импорта!
# Обратить внимание на сообщение с изменениями после пула
# и попросить посмотреть лог.
step6: step5
	cd $(USER1)
	cp $(ASSETS)/02-01-homework_notebook.Rmd homework_notebook.Rmd
	cp $(ASSETS)/02-02-homework_notebook.Rmd homework_notebook.Rmd
	git add .
	git commit -m "Импортировали данные"
	git push
	cd $(USER2) && git pull
	cd $(USER3) && git pull
	cd $(USER4) && git pull

# Каждый подписывает свои имена напротив заданий
# TODO: Текст коммита

step7_user2:
	cd $(USER2)
	git checkout -b user2
	cp $(ASSETS)/03-02-homework_notebook.Rmd homework_notebook.Rmd
	git add .
	git commit -m "Подписал задания"
	git push -u --force origin user2
	gh pr create --title "Подписал задания" --body ""

step7_user3:
	cd $(USER3)
	git checkout -b user3
	cp $(ASSETS)/03-03-homework_notebook.Rmd homework_notebook.Rmd
	git add .
	git commit -m "Подписал задания"
	git push -u --force origin user3
	gh pr create --title "Подписал задания" --body ""

step7_user4:
	cd $(USER4)
	git checkout -b user4
	cp $(ASSETS)/03-04-homework_notebook.Rmd homework_notebook.Rmd
	git add .
	git commit -m "Подписал задания"
	git push -u --force origin user4
	gh pr create --title "Подписал задания" --body ""

step7_user1:
	cd $(USER1)
	gh pr merge --merge user2
	gh pr merge --merge user3
	gh pr merge --merge user4

# Все синкаются, для практики, в том числе координатор
step7_pull:
	cd $(USER1) && git checkout main && git pull
	cd $(USER2) && git checkout main && git pull
	cd $(USER3) && git checkout main && git pull
	cd $(USER4) && git checkout main && git pull

step7: step6 step7_user2 step7_user3 step7_user4 step7_user1 step7_pull

# Каждый делает по заданию
# TODO: Текст коммита

step8_2:
	cd $(USER2)
	git checkout -b describe
	cp $(ASSETS)/04-02-homework_notebook.Rmd homework_notebook.Rmd
	git add .
	git commit -m "Посчитал описательные статистики"
	git push -u --force origin describe
	gh pr create --title "Посчитал описательные статистики" --body ""

step8_3:
	cd $(USER3)
	git checkout -b boxplot
	cp $(ASSETS)/04-03-homework_notebook.Rmd homework_notebook.Rmd
	git add .
	git commit -m "Нарисовал boxplot"
	git push -u --force origin boxplot
	gh pr create --title "Нарисовал boxplot" --body ""
