SHELL := /bin/bash
CURRENT_DIR = $(shell pwd)

commit:
	python src/manage.py makemigrations ${app}
