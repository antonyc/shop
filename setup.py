# coding: utf-8

from setuptools import setup, find_packages


setup(
    name='pets_application',
    description='Backend for pets application',
    long_description='',
    author='Chaporgin Anton',
    author_email='mrdark@list.ru',
    packages=find_packages(),
    package_dir={'': ''},
    # include_package_data=True,
    # zip_safe=True,
    version='0.1',
    # py_modules=['sitecustomize']  # added additional single module from root 'src' folder
)
