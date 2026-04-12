IMAGE_NAME = gist-api
IMAGE_TAG = latest
PORT = 8080

.PHONY: build run run-detached stop test clean logs

build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

run:
	docker run -p $(PORT):$(PORT) --name $(IMAGE_NAME) $(IMAGE_NAME):$(IMAGE_TAG)

run-detached:
	docker run -d -p $(PORT):$(PORT) --name $(IMAGE_NAME) $(IMAGE_NAME):$(IMAGE_TAG)

stop:
	docker stop $(IMAGE_NAME) && docker rm $(IMAGE_NAME)

test:
	pytest test_app.py -v

logs:
	docker logs -f $(IMAGE_NAME)

clean:
	docker stop $(IMAGE_NAME) || true
	docker rm $(IMAGE_NAME) || true
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true

.DEFAULT_GOAL := build