launch-database:
	docker run --rm -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=s3cr3t -e MONGO_INITDB_DATABASE=iot -p 27017:27017 mongo:4.4.2

build-image:
	docker build -t corka149/iotserver:latest .

release-image: build-image
	docker push corka149/iotserver:latest

run-standalone: build-image
	docker-compose down
	docker-compose pull
	docker-compose up
