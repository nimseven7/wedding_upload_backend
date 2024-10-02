STAGE ?= dev
DOCKERFILE = backend.Dockerfile

DOCKER_IMAGE = wedup-backend
.PHONY: build

default: build

build:
	@echo "Building..."
	docker build -t $(DOCKER_IMAGE) -f $(DOCKERFILE) .