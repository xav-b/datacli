# Common.mk
# vim:ft=make
#
# Documentation guidelines :http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
#
#  Configuration  #############################################################

.DEFAULT_GOAL := help

PROJECT    := $(shell basename $(PWD))
BUILD_TIME := $(shell date +%FT%T%z)

GIT_COMMIT := $(shell git rev-parse HEAD)
GIT_USER   := $(shell git config --get user.name)

# docker-compose based container name
CONTAINER  := "$(GIT_USER)/$(PROJECT)"

###############################################################################

.PHONY: love
love:
	@echo "not war !"

.PHONY: help
help: ## print this message
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)''

.PHONY: tasks
tasks: ## grep TODO and FIXME project-wide
	@grep --exclude-dir=.git --exclude-dir=node_modules -rEI "TODO|FIXME" .

.PHONY: container
container: ## build a container from the local Dockerfile
	docker build --rm -t appturbo/$(PROJECT) .

.PHONY: deploy
deploy: ## push staging code on Elastic Beanstalk
	git add -A
	eb deploy --staged --timeout 3600