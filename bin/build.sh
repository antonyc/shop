#!/bin/sh
APP_NAME=amadika_shop

VERSION=$(dpkg-parsechangelog | sed -nr 's/^Version: ([0-9\.]+)\-[0-9]+/\1/p')
FOLDER_NAME=${APP_NAME}-${VERSION}

# detect branch to build
BRANCH=$(git branch|grep \*| sed 's/\* //g')

echo "Building branch ${BRANCH}..."

rm -rf ./.build
mkdir ./.build
cd ./.build

git clone -b $BRANCH /home/chapson/amadika/amadika-shop-0.1 $FOLDER_NAME
TARNAME=amadika-shop
cd $FOLDER_NAME

cp -f src/local_settings.py.example src/local_settings.py
src/manage.py collectstatic --noinput -v0
src/manage.py synccompress --force -v0
rm src/local_settings.py
find . -name "*.pyc" -delete
cd ..
tar --exclude=debian -czf ${TARNAME}_0.1.orig.tar.gz $FOLDER_NAME
cd $FOLDER_NAME
debuild --no-lintian 

cd ..
