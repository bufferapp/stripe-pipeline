.DEFAULT_GOAL := help

IMAGE_NAME := bufferapp/stripe-pipeline:0.1.0

.PHONY: help
help:
	@echo -e "Usage: \tmake [TARGET]\n"
	@echo -e "Targets:"
	@echo -e "  deps            Installs and checks for dependencies (Pipenv)"
	@echo -e "  init            Initialize the Python enviroment, make sure to run this before using make run"
	@echo -e "  run             Execute the crawler locally"
	@echo -e "  console         Open a IPython console for testing and development"
	@echo -e "  image           Build crawler Docker image"
	@echo -e "  rund            Execute the crawler in a Docker container"
	@echo -e "  push            Push crawler Docker image to the registry"
	@echo -e "  deploy          Deploy the crawler to Kubernetes"

.PHONY: deps
deps:
	@pip install pipenv
	@docker -v

.PHONY: init
init: deps
	@pipenv install --dev

.PHONY: run
run:
	@pipenv run stripe-pipeline crawler run

.PHONY: image
image:
	@docker build -t $(IMAGE_NAME) .

.PHONY: rund
rund: image
	docker run --env-file .env --rm $(IMAGE_NAME) crawler run

.PHONY: push
push: image
	@docker push $(IMAGE_NAME)

.PHONY: deploy
deploy: push
	echo "Not implemented yet!"
	#@kubectl apply -f crawler.deployment.yaml

.PHONY: console
console:
	@pipenv run ipython
