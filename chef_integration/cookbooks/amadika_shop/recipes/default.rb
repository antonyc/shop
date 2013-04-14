#
# Cookbook Name:: amadika_uni_src
# Recipe:: default
#
# Copyright 2013, Amadika
#
# All rights reserved - Do Not Redistribute
#


require_recipe "python"

app = data_bag_item("apps", "amadika_uni_src")

developer = data_bag_item("users", "vagrant")

#python_virtualenv app["virtualenv"] do
#    owner developer.id
#	group developer["groups"].first
#	interpreter "python2.7"
#	action :create
#end

python_pip "django" do
  version "1.5"
  action :install
end

%w{g++ perl python python-dev python-setuptools python-imaging re2c nginx}.each do |pkg|
  package pkg do
    action :install
  end
end


%w{memcached mongodb python-mysqldb python-lxml libgeos-c1 python-gdal re2c libgdal1-1.6.0 g++}.each do |pkg|
  package pkg do
    action :install
  end
end

python_pip "pyparsing" do
  version "1.5.6"
  action :install
end

python_pip "mwlib" do
  version "0.12.14"
  action :install
end

%w{beautifulsoup pysqlite simplejson PIL django_dynamic_fixture django_mptt pymongo trans flup south}.each do |pkg|
  python_pip pkg do
    action :install
  end
end

service "memcached" do
  supports :restart => true, :status => true
  action [ :enable, :start ]
end

service "mongodb" do
  supports :restart => true, :status => true
  action [ :enable, :start ]
end

execute "create_database" do
    cwd "/vagrant"
    command "/vagrant/src/manage.py test"
end

# /vagrant/src/university/manage.py syncdb --settings=university.local_settings
# /vagrant/src/university/manage.py migrate --settings=university.local_settings

#execute "create_database" do
#  cwd "/vagrant"
#  command "src/university/manage.py syncdb --settings=university.local_settings --noinput"
#  command "src/university/manage.py dbshell --settings=university.local_settings"
#end
