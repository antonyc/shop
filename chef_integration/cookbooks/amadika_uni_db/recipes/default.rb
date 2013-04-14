#
# Cookbook Name:: amadika_database
# Recipe:: default
#
# Copyright 2012, Amadika
#
# All rights reserved - Do Not Redistribute
#

app = data_bag_item("apps", "amadika_uni_db")

root_password = node.normal.mysql.server_root_password
database = app["databases"]["default"]
database_name = database["name"]
database_user = database["username"]
database_password = database["password"]

server_user_name = 'server_' + database_user + '_password'

if !node['mysql'][server_user_name]
	# создать пользователя и базу данных
	execute <<-EOS
		echo "CREATE DATABASE IF NOT EXISTS #{database_name} DEFAULT CHARSET 'utf8';" | \
		mysql -uroot -p#{root_password}
	EOS

	execute <<-EOS
		echo "GRANT ALL ON #{database_name}.* TO #{database_user}@localhost IDENTIFIED BY '#{database_password}'" | \
		mysql -uroot -p#{root_password}
	EOS

	node.set['mysql'][server_user_name] = database_password
	
end
