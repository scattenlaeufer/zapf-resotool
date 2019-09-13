# zapf-resotool
<a href="https://github.com/python/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

A bit of software to manage ZaPF resolutions

## Hacking

To develop resotool you will need `python` (`3.7+`) and
[poetry](https://github.com/sdispater/poetry).

To start help developing `resotool` run
```
poetry install
```
to install all development dependencies.

Currently the database is sqlite, but will at some point be moved to
PostgreSQL.

To start change into the toplevel `resotool` and run
```
make migration
```
which runs
```
poetry run ./manage.py makemigrations
poetry run ./manage.py migrate
```
to initalise the database, after which you can start hacking :)

Run `make test` (or `poetry run pytest`) to run the tests and `make server` (or
`poetry run ./manage.py runserver`) to run the development server.

### pre-commit

We are using [pre-commit](https://github.com/pre-commit/pre-commit) to enforce
our coding style.

Install pre-commit via your system package manager or `pip install --user pre-commit`
and `pre-commit install` in this repository to enable the git hooks,
pre-commit will then run on every commit.

For more information have a look at the [pre-commit docs](https://pre-commit.com/#usage).

## Settings

> **WARNING**: Do not change `CELERY_EMAIL_CHUNK_SIZE`! The current setting of
> `1` is required for the correct setting of the send status of sent mails.

## Testing

To run all of the test, an instance of Celery must be running. From `resotool`,
this can either be achieved by running `make celery-run` for a simple Celery
worker or `make celery-start` for a detached celery worker, which can be
stopped with `make celery-stop` after running the tests. If no Celery instance
is running, all tests requiring Celery will be skipped.

### Celery mails

Since resotool uses a separate back end to send mails using Celery and Django
replaces the set email back end with the `locmem` back end, there is a separate
test to check whether sending mails through Celery is working correctly.

To do this, a settings file must be created with the credentials of the
mailboxes used for testing. The path to this file must be
`resotool/resoapp/tests/celery_mail_test_settings.toml` and the file has the
following structure:
```
[out]
server = "SERVER"
port = PORT
account = "ACCOUNT_NAME"
password = "PASSWORD"
email = "EMAIL"

[in]
server = "SERVER"
port = PORT
account = "ACCOUNT_NAME"
password = "PASSWORD"
email = ["EMAIL_1", "EMAIL_2", ...]
```
In this case `[out]` defines the mailbox from which the mails are to be sent,
while `[in]` defines the mailbox receiving the mails. The test overrides the
those email settings from `resotool/settings.py`, so to run this test, you must
create this file with the required infos.  If the file can't be found, the test
will be skipped.
