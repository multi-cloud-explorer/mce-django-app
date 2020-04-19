# Multi-Cloud Explorer - Django App

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.org/multi-cloud-explorer/mce-django-app.svg)](https://travis-ci.org/multi-cloud-explorer/mce-django-app)
[![Coverage Status](https://coveralls.io/repos/github/multi-cloud-explorer/mce-django-app/badge.svg?branch=master)](https://coveralls.io/github/multi-cloud-explorer/mce-django-app?branch=master)
[![Code Health](https://landscape.io/github/multi-cloud-explorer/mce-django-app/master/landscape.svg?style=flat)](https://landscape.io/github/multi-cloud-explorer/mce-django-app/master)
[![Requirements Status](https://requires.io/github/multi-cloud-explorer/mce-django-app/requirements.svg?branch=master)](https://requires.io/github/multi-cloud-explorer/mce-django-app/requirements/?branch=master)

[Documentation](https://multi-cloud-explorer.readthedocs.org)

## Integrate in your Django Project

**Install:**

```bash
pip install git+https://github.com/multi-cloud-explorer/mce-django-app.git
```

**Add to settings.py:**

```python
INSTALLED_APPS = [
    ...,
    'mce_django_app',
]
```

**Update database:**

```bash
./manage.py migrate
```

## Run Tests

```bash

pip install -e .[tests]

# With sqlite:
./manage.py test

# With PostgreSQL:
DATABASE_URL=postgres://mce:password@127.0.0.1:5432/mce ./manage.py test
```

