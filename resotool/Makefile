ifneq ("$(wildcard $(HOME)/.poetry/bin/poetry)", "")
	POETRY := $(HOME)/.poetry/bin/poetry
else
	POETRY := /usr/bin/poetry
endif

POETRY_RUN := $(POETRY) run

test:
	$(POETRY_RUN) pytest

migration:
	$(POETRY_RUN) ./manage.py makemigrations
	$(POETRY_RUN) ./manage.py migrate

server:
	$(POETRY_RUN) ./manage.py runserver
