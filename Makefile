SHELL := /bin/bash
MACHINE_NAME ?= rittenhouse
MACHINE_CPU_COUNT ?= 1
MACHINE_DISK_SIZE ?= 30000
MACHINE_MEMORY ?= 1024
RUN_CMD = docker-compose run --rm

.PHONY: clean machine server stop

check:
	@if docker-machine status ${MACHINE_NAME} | grep Stopped > /dev/null; then \
		echo 'The Docker machine "${MACHINE_NAME}" is not active. Start it with the following command:'; \
		echo ''; \
		echo '  $$ eval "$$(make machine)"'; \
		exit 1; \
	fi

clean: check
	docker-compose kill > /dev/null 2>&1 || :
	docker-compose rm -f > /dev/null 2>&1 || :
	docker rm $$(docker ps -aq) > /dev/null 2>&1 || :
	docker rmi $$(docker images --filter=dangling=true -q) > /dev/null 2>&1 || :

machine:
	@if ! docker-machine status ${MACHINE_NAME} > /dev/null 2>&1; then \
		echo "# Creating machine..."; \
		docker-machine create \
			--driver virtualbox \
			--virtualbox-cpu-count ${MACHINE_CPU_COUNT} \
			--virtualbox-disk-size ${MACHINE_DISK_SIZE} \
			--virtualbox-memory ${MACHINE_MEMORY} \
			${MACHINE_NAME} > /dev/null; \
	elif docker-machine status ${MACHINE_NAME} | grep Stopped > /dev/null; then \
		echo "# Starting machine..."; \
		docker-machine start ${MACHINE_NAME} > /dev/null; \
		docker-machine regenerate-certs -f ${MACHINE_NAME} > /dev/null; \
	fi
	@docker-machine env ${MACHINE_NAME}

server: check clean
	docker-compose build web
	docker-compose up -d web
	@echo "The server is reachable at: "
	@echo "http://$$(docker-machine ip ${MACHINE_NAME}):5000"

stop:
	docker-machine stop ${MACHINE_NAME}
