from setuptools import setup, find_packages

install_requires = [
    'Django>=3.0',
    'django-extensions',
    'django-cryptography',
    'django-model-utils',
]

tests_requires = [
    'pytest',
    'pytest-cov',
    'pytest-pep8',
    'pytest-django',
    'pytest-timeout',
    'django-dynamic-fixture',
    'pytest-instafail',
    'curlify',
    'factory-boy',
    'bandit',         # python security audit
    'flake8',
    'coverage',
    'responses',
    'freezegun',
]

dev_requires = [
    'pylint',
    'ipython',
    'autopep8',
    'black',
]

doc_requires = [
    'Sphinx',
    'sphinx_rtd_theme',
    'sphinx-click',
]

extras_requires = {
    'tests': tests_requires,
    'dev': dev_requires,
    'doc': doc_requires,
}

setup(
    name='mce-django-app',
    version="0.1.0",
    description='Django App for Multi Cloud Explorer',
    url='https://github.com/srault95/mce-django-app.git',
    packages=find_packages(),
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
