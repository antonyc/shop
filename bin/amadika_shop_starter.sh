#! /bin/sh
### BEGIN INIT INFO
# Provides:          amadika_shop
# Required-Start:    $local_fs $remote_fs
# Required-Stop:     $local_fs $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      S 0 1 6
# Short-Description: Amadika Shop FastCGI daemon
# Description:       This file starts amadika shop daemons
### END INIT INFO

set -e

case "$1" in
  start) 
    mkdir -p /var/run/amadika/shop
    chown www-data /var/run/amadika/shop
    sudo -u www-data /usr/lib/amadika/shop/manage.py runfcgi method=prefork socket=/var/run/amadika/shop/fcgi.sock pidfile=/var/run/amadika/shop/run.pid 
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
