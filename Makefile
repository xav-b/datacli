# Makefile
# vim:ft=make

include ./Python.mk

container.init:
	@docker-compose up -d
	@./container-init.sh
