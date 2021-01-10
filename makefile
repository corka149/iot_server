# DEVELOPMENT
test:
	pip install -q pytest tox
	tox

format:
	pip install -q autopep8
	autopep8 -r --in-place --aggressive --aggressive --max-line-length 100 src/iot_server

check:
	pip install -q mypy pylint pylint-mongoengine
	mypy src
	pylint --load-plugins=pylint_mongoengine src

# DOCKER
launch-database:
	docker run --rm -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=s3cr3t -e MONGO_INITDB_DATABASE=iot -p 27017:27017 mongo:4.4.2

build-image:
	docker build -t corka149/iotserver:latest .

release-image: build-image test
	docker push corka149/iotserver:latest

run-standalone: build-image
	docker-compose down
	docker-compose pull
	docker-compose up
