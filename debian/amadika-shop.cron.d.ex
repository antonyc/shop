#
# Regular cron jobs for the amadika-shop package
#
0 4	* * *	root	[ -x /usr/bin/amadika-shop_maintenance ] && /usr/bin/amadika-shop_maintenance
