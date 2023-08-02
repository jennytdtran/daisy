#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

requirements = [
    "Django==4.2.3",
    "django-auth-ldap==4.4.0",

    "celery==5.2.3",
    "celery-haystack-ng",
    "django-celery-beat==2.5.0",
    "django-celery-results==2.4.0",

    'django-model-utils==4.2.0',
    'django-sequences==2.2',
    'django-enumchoicefield==3.0',

    'django-compressor==2.2',
    'django-debug-toolbar==3.2.1',
    'django-formtools==2.1',
    'django-widget-tweaks==1.4.3',
    'django-countries==7.3.2',

    'django-haystack==3.1',
    'django-reversion==3.0.3',
    'django-guardian==2.4.0',
    'django-stronghold==0.3.0',
    'gunicorn==19.9.0',
    'ipython==7.16.3',
    'ontobio==2.8.3',
    'yamldown>=0.1.8',
    'psycopg2-binary==2.9.3',
    'pysolr==3.8.1',
    'pytest-runner==5.1',
    'python-keycloak==2.6.0',
    'pytz==2022.1',
    'requests==2.25.1',
    'urllib3==1.26.5',
    'setuptools-scm==3.3.3',
    'jsonschema==3.2.0',
    'mockldap@git+https://github.com/elixir-luxembourg/mockldap2.git',
    'django-auditlog==2.1.1',
]

test_requirements = [
    'coverage==6.4.1', 
    'factory_boy==3.2.1',
    'pytest==7.1.2', 
    'pytest-django==4.5.2', 
    'pytest-solr==1.0a1', 
    'pytest-celery'
]

dev_requirements = [
]

setup(
    name='elixir-daisy',
    version='1.7.12',
    description="Elixir-LU DAISY",
    author="Pinar Alper, Valentin Grouès, Yohan Jarosz, Jacek Lebioda, Kavita Rege, Vilem Ded",
    author_email='lcsb.sysadmins@uni.lu',
    url='https://github.com/elixir-luxembourg/daisy',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    package_dir={'elixir_daisy':
                     'elixir_daisy'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords=['elixir', 'gdpr', 'data protection'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    package_data={
        'elixir-daisy': ['elixir_daisy/resources/*']
    },
    extras_require={
        'dev': dev_requirements
    },
    scripts=['manage.py']
)
