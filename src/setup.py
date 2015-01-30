# coding: utf-8
import os
from setuptools import setup, find_packages, findall


def data_files(dirname):
    """
    Собрать все дата-файлы.
    """
    settings_dir = os.path.join(dirname, 'settings')
    ALLOWED_EXTENSIONS = (
        '.json', '.html', '.txt', '.json', '.xml'
    )
    for another_file in findall(dirname):
        if os.path.splitext(another_file)[-1] in ALLOWED_EXTENSIONS:
            yield another_file
        elif another_file.startswith(settings_dir):
            # включить всю папку settings
            yield another_file


setup(
    name='wiki-shop',
    description='Amadika wiki-shop',
    author='Anton Chaporgin',
    author_email='chapson@amadika.ru',
    packages=find_packages(),
    package_data={
        'shop': [filename[len('shop/'):] for filename in data_files('shop')],
    },
    entry_points={
        'console_scripts': [
            #'wiki_manage = shop.manage:management',
        ],
    },
)
