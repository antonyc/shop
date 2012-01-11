MAILTO=chaporginanton@yandex.ru
* * * * * www-data python /usr/lib/amadika/shop/manage.py mail_users -v0
0 0 */2 * * www-data python /usr/lib/amadika/shop/manage.py sitemap -v0 --pages=10000 --output=/usr/share/amadika/shop/media/sitemap.xml
5 0 */2 * * www-data python /usr/lib/amadika/shop/manage.py ping_google /media/sitemap.xml

