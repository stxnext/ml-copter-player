venv:
	python3.6 -m venv venv

install:
	venv/bin/pip install -r requirements.txt

run:
	PYTHONPATH=. venv/bin/python -m app

clean_db:
	mongo sensors-db --eval 'db.sensors_data.drop()'

interpreter:
	PYTHONPATH=. venv/bin/python

teach:
	PYTHONPATH=. venv/bin/python -m teach

docker_build:
	USER_ID=`id -u` docker-compose build

docker_up:
	USER_ID=`id -u` docker-compose up -d

docker_down:
	USER_ID=`id -u` docker-compose down

docker_teach:
	USER_ID=`id -u` docker-compose exec game python3.6 teach.py

