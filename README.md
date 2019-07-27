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
poetry ./manage.py makemigrations
poetry ./manage.py migrate
```
to initalise the database, after which you can start hacking :)

Run `make test` (or `poetry run pytest`) to run the tests and `make server` (or
`poetry run ./manage.py runserver`) to run the development server.
