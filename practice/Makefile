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

clean:
	rm -fr $(ROOT)
	gh repo delete --yes $(GITHUB) || true

step0:
	mkdir -p $(ROOT)

# Создаем проект
step1_user1: step0
	unzip assets/project.zip -d $(ROOT)

step1: step0 step1_user1

# Создаем коммит
step2_user1: step1
	cd $(USER1)
	git add .
	git commit -m "Создали проект R"

step2: step1 step2_user1

# Создаем ПРИВАТНЫЙ репозиторий
step3_user1: step2
	cd $(USER1)
	gh repo create --private $(GITHUB)
	git remote add origin $(REMOTE)
	git branch -M main
	git push -u --force origin main

step3: step2 step3_user1

# Добавляем участников в репу, в том числе меня
# Обратить внимание координаторов на то, чтобы инвайты были приняты
step4_user1:

# Все клонируют (кроме ведущего)
step4_user234: step3
	git clone $(REMOTE) $(USER2)
	git clone $(REMOTE) $(USER3)
	git clone $(REMOTE) $(USER4)

step4: step3 step4_user1 step4_user234
