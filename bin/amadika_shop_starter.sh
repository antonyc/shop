#!/bin/bash

case "$1" in
  start) 
    /usr/lib/amadika/shop/manage.py runfcgi method=prefork socket=/var/run/amadika/shop/fcgi.soc pidfile=/var/run/amadika/shop/run.pid 
    ;;
  stop) 
    kill -9 `cat /var/run/amadika/shop/run.pid` 
    ;;
  restart)
    $0 stop
    sleep 1
    $0 start
    ;;
  *) echo "Usage: ./server.sh {start|stop|restart}";;
esac
