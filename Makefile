# DEVELOPMENT
test:
	pip install -q pytest tox
	tox

format:
	pip install -q black
	black src/iot_server

check:
	pip install -q mypy pylint pylint-mongoengine
	mypy src
	pylint --load-plugins=pylint_mongoengine src

# DOCKER
launch-database:
	docker-compose up -d mongo redis

build-image:
	docker build -t corka149/iotserver:latest .

release-image: build-image test
	docker push corka149/iotserver:latest

run-standalone: build-image
	docker-compose down
	docker-compose pull
	docker-compose up
