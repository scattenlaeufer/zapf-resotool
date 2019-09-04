ifneq ("$(wildcard $(HOME)/.poetry/bin/poetry)", "")
	POETRY := $(HOME)/.poetry/bin/poetry
else
	POETRY := /usr/bin/poetry
endif

POETRY_RUN := $(POETRY) run
CELERY_INSTANCE := celery_instance_1
CELERY_MODULE := resotool.celery
CELERY_LOGLEVEL := info

test:
	$(POETRY_RUN) pytest

migration:
	$(POETRY_RUN) ./manage.py makemigrations
	$(POETRY_RUN) ./manage.py migrate

celery-start:
	$(POETRY_RUN) celery multi start $(CELERY_INSTANCE) -A $(CELERY_MODULE) --loglevel=$(CELERY_LOGLEVEL)

celery-stop:
	$(POETRY_RUN) celery multi stop $(CELERY_INSTANCE)

celery-run:
	$(POETRY_RUN) celery -A $(CELERY_MODULE) worker --loglevel=$(CELERY_LOGLEVEL)

server:
	$(POETRY_RUN) ./manage.py runserver

start-server: celery-start server celery-stop

shell:
	$(POETRY_RUN) ./manage.py shell

dummy-data:
	$(POETRY_RUN) ./create_dummy_resos.py
