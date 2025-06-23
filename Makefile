SHELL := /bin/bash
CURRENT_DIR = $(shell pwd)

commit:
	docker exec -it xtweb_main python src/manage.py makemigrations ${app}

migrate:
	docker exec -it xtweb_main python src/manage.py migrate

passwd:
	docker exec -it xtweb_main python src/manage.py changepassword ${user}

adduser:
	docker exec -it xtweb_main python src/manage.py createsuperuser ${user}

shell:
	docker exec -it xtweb_main python src/manage.py shell
