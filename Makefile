build:
			@# build - build docker images and build containers.
			$(info Начинаю установку...)
			cd videorender && \
			docker-compose build && \
			docker-compose run --rm web python manage.py makemigrations && \
			docker-compose run --rm web python manage.py migrate
	
			#sudo docker-compose build && \
			#sudo docker-compose run --rm web python manage.py makemigrations && \
			#sudo docker-compose run --rm web python manage.py migrate

lsc:
			@# lsc - "LiSt containers".
			$(info Текущие контейнеры:)
			docker ps -a

lsi:
			@# lsi - "LiSt images".
			$(info Текущие образы:)
			docker images

up:
			@# up - up and running docker containers
			$(info Поднимаем контейнеры)
			cd videorender && docker-compose up

clearc:
			@# clearc - "clear container" 'videorender_web_1' and 'videorender_db_1'
			$(info Удаляем текущие контейнеры...)
			docker rm -f videorender_web_1
			docker rm -f videorender_db_1

clearv:
			@# clearv - "clear volumes" 'videorender'
			$(info Удаляем все созданные образы...)
			docker rmi videorender:dev
			docker rmi postgres:9.6.9-alpine
			docker rmi python:3.8.9-slim-buster


clearall:
			@# clearall - clear all docker containers and images.
			$(info Удаляю  всё...)
			sudo docker rm -f $$(sudo docker ps -a -q)
			sudo docker rmi $$(sudo docker images -q)


venv:
			@# venv - install PIP, virtual environment pakeges and depedencies
			$(info Устанавливаю окружение и зависимости...)
			sudo apt install python3-pip curl -y
			python3 -m pip --version
			python3 -m pip install --upgrade pip 
			python3 -m pip install virtualenv
		   	python3 -m venv env38
			./poetryInstall.bash	

runserver:
			@# runserver - Start server application and kafka queur by python (localy).
			python videorender/manage.py runserver

help:
			@# help - Show this help.
			@./MakefileHelp.sh


