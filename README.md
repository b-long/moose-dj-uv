# moose-dj-uv

## About

## Tooling

This project was created with `uv init moose-dj-uv`, and 
is being used to learn `uv`.

For additional information, see: 
* https://docs.astral.sh/uv/guides/projects/

### Django with `uv` ... `startproject`

Execute the `django-admin` CLI

```
uv run django-admin --help
```

Django projects can be created like below:

```
uv run django-admin startproject moose_dj .
```

### Django with `uv` ... `startapp`

Next, inside the project create an app:

```bash
cd moose_dj

uv run django-admin startapp news

# -~*-~*-~* Remember -~*-~*-~*
# Update the 'AppConfig', with the namespaced
# module name, e.g. 'moose_dj.news'

# class NewsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'moose_dj.news'
```

### Django with `uv` ... `pytest` (requires `makemigrations` )

```
uv run manage.py check
uv run manage.py makemigrations
uv run pytest
```

#### Dependency installations: Prod

To install production dependencies, run:

```
uv sync --no-dev --locked
```

#### Dependency installations: Prod


To install dependencies in CI, run:

```
uv sync --locked
```
