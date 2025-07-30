VENV := .venv
REQUIREMENTS_PATH := requirements/requirements-dev.txt
MANAGE_PATH := manage.py


$(VENV)/bin/activate: $(REQUIREMENTS_PATH)
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r $(REQUIREMENTS_PATH)
	. $(VENV)/bin/activate

install: $(VENV)/bin/activate

makemigrations: install
	. $(VENV)/bin/activate && python3 $(MANAGE_PATH) makemigrations


migrate: makemigrations
	. $(VENV)/bin/activate &&  python3 $(MANAGE_PATH) migrate

build: migrate

runserver:
	. $(VENV)/bin/activate && python3 $(MANAGE_PATH) runserver


.PHONY: build, install, makemigrations, migrate, runserver