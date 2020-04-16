import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

install_requires = [
    'Django>=3.0',
    'django-extensions',
    'django-cryptography',
    'django-model-utils',
    'django-guardian',
    'python-slugify',
    'djangorestframework',

    'django-dynamic-fixture', # for mce_django_app.pytest.plugin
    'pytest',                 # for mce_django_app.pytest.plugin
]

tests_requires = [
    'psycopg2-binary',
    'pytest',
    'pytest-cov',
    'pytest-pep8',
    'pytest-django',
    'pytest-timeout',
    'django-dynamic-fixture',
    'pytest-instafail',
    'curlify',
    'factory-boy',
    'bandit',
    'flake8',
    'coverage',
    'responses',
    'freezegun',

    'django-environ',
    'django-filter',
    'django-select2',
    'django-crispy-forms',

    'django-cors-headers',
    'djoser',
    'drf-yasg',

    'django-allauth',

    'jsonpatch'
]

dev_requires = [
    'pylint',
    'ipython',
    'autopep8',
    'black',
    'wheel',
]

extras_requires = {
    'tests': tests_requires,
    'dev': dev_requires,
}

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mce-django-app',
    version="0.1.0",
    description='Django App for Multi Cloud Explorer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/multi-cloud-explorer/mce-django-app.git',
    license='GPLv3+',
    packages=find_packages(exclude=("tests",)),
    include_package_data=False, 
    tests_require=tests_requires,
    install_requires=install_requires,
    extras_require=extras_requires,
    test_suite='tests',
    zip_safe=False,
    author='Stephane RAULT',
    author_email="stephane.rault@radicalspam.org",
    python_requires='>=3.7',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    #entry_points = {
    #    "pytest11": ["mce_django_app = mce_django_app.pytest.plugin"]
    #},
)
