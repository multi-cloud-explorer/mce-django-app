import os
from setuptools import setup, find_packages

import versioneer

install_requires = [
    'wheel',
    'Django>=3.0',
    'django-extensions',
    'django-cryptography',
    'python-slugify',
    'furl',
    'jsonpatch>=1.25,<2',
    'djangorestframework',
    'django-daterangefilter',
    'django-filter',
    'django-select2',
    'jsonfield',
    'tabulate', # commands
    'django-taggit',
    'django-mptt',
    'django-formtools',
    'django-admin-tools@git+https://github.com/yakky/django-admin-tools.git@feature/django-30#egg=django-admin-tools',

    'django-redis',
    #'gevent',

    'django-dynamic-fixture>=3.1.0', # for mce_django_app.pytest.plugin
    'pytest>=5.4.1',                 # for mce_django_app.pytest.plugin
]

mce_lib_requires = [
    'mce-lib-azure@git+https://github.com/multi-cloud-explorer/mce-lib-azure.git@master#egg=mce_lib_azure',
    'mce-lib-vsphere@git+https://github.com/multi-cloud-explorer/mce-lib-vsphere.git@master#egg=mce_lib_vsphere',
    #'mce-lib-gcp@git+https://github.com/multi-cloud-explorer/mce-lib-gcp.git@master#egg=mce_lib_gcp',
    'mce-lib-aws@git+https://github.com/multi-cloud-explorer/mce-lib-aws.git@master#egg=mce_lib_aws',
]
install_requires.extend(mce_lib_requires)

tests_requires = [
    'psycopg2-binary',
    'pytest>=5.4.1',
    'pytest-cov',
    'pytest-pep8',
    'pytest-django',
    'pytest-timeout',
    'django-dynamic-fixture>=3.1.0',
    'pytest-instafail',
    'curlify',
    'factory-boy',
    'bandit',
    'flake8',
    'coverage',
    'responses',
    'freezegun',
    'docker',

    'jsonpatch',
    'django-environ',
    'django-filter',
    'django-select2',
    'django-allauth',

    'django-cors-headers',
    'djoser',
    'drf-yasg',

]

dev_requires = [
    'pylint',
    'ipython',
    'autopep8',
    'black',
    'wheel',
    'pipdeptree',
    'django-debug-toolbar',
    'pygraphviz',
    'pydotplus',
    'safety',
]

ci_requires = [
    'coveralls',
    'codecov',
]

extras_requires = {
    'tests': tests_requires,
    'dev': dev_requires,
    'ci': ci_requires
}

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mce-django-app',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Django App for Multi Cloud Explorer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/multi-cloud-explorer/mce-django-app.git',
    license='GPLv3+',
    packages=find_packages(exclude=("tests",)),
    include_package_data=True, 
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
