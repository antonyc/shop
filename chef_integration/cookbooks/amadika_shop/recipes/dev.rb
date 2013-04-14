#
# Cookbook Name:: amadika_uni_src
# Recipe:: default
#
# Copyright 2012, Amadika
#
# All rights reserved - Do Not Redistribute
#

include_recipe 'amadika_uni_src::environment'

app = data_bag_item("apps", "amadika_uni_src")
db = data_bag_item("apps", "amadika_uni_db")
developer = data_bag_item("users", "developer")

# создаем папку проекта
www_path = File.join(app["virtualenv"], "www")

# папка с настройками local_settings.py
settings_path = File.join(app["virtualenv"], "settings")

# папка для закачивания всякого
media_root = File.join(app["virtualenv"], "media")

[ www_path, settings_path, media_root ].each do |path|
	if !File.exist?(path)
		Dir.mkdir(path)
	end	
	File.chown(node.etc.passwd[developer.id].uid, node.etc.group[developer["groups"].first].gid, path)
end

File.chmod(0550, settings_path)

#local_settings.py
database = db["databases"]["default"]
template File.join(settings_path, "local_settings.py") do
  source "local_settings.py.erb"
  mode 0440
  owner developer.id
  group developer["groups"].first
  variables(
    :media_root => media_root,
    :www_path => www_path,
		:mysql_password => database["password"],
		:mysql_name => database["name"],
		:mysql_username => database["username"]
  )
end

include_recipe "git::default"

# обновляем репозиторий с кодом
web_project_path = File.join(www_path, "university")
if !File.exists(web_project_path)
  execute "clone web front code" do
    command "git clone " << app["git"] << " " << web_project_path
  end
else
  execute "pull web front code" do
    cwd web_project_path
    command "git pull origin"
  end
end
