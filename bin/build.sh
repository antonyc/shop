#!/bin/sh
APP_NAME=amadika_shop

VERSION=$(dpkg-parsechangelog | sed -nr 's/^Version: ([0-9\.]+)\-[0-9]+/\1/p')
FOLDER_NAME=${APP_NAME}-${VERSION}

# detect branch to build
BRANCH=$(git branch|grep \*| sed 's/\* //g')

echo "Building branch ${BRANCH}..."

rm -rf .build
make .build
cd .build

git clone -b $BRANCH /home/chapson/amadika/amadika-shop-0.1 $FOLDER_NAME
cd $FOLDER_NAME

cp -f src/local_settings.py.example src/local_settings.py
src/manage.py collectstatic --noinput -v0
src/manage.py synccompress --force -v0
rm dj/local_settings.py

debuild --no-lintian --no-tgz-check

cd ..
