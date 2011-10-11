#!/bin/bash

rm -rf static/*
src/manage.py collectstatic --noinput -v0
rm -rf static/admin
src/manage.py synccompress --force -v0
