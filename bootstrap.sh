#!/usr/bin/env bash
source /home/vagrant/django-vagrant/.env
sudo apt-get update
sudo apt-get -y upgrade

sudo apt-get -y install python-dev
sudo apt-get -y install libpq-dev
sudo apt-get -y install libffi-dev libssl-dev libxml2-dev libxslt1-dev
sudo apt-get -y install libxmlsec1 libxmlsec1-dev swig
sudo apt-get -y install libjpeg-dev libpng12-dev
sudo apt-get -y install python-lxml python-cffi libcairo2 libpango1.0-0 libgdk-pixbuf2.0-0 shared-mime-info

sudo apt-get -y install redis-server

sudo apt-get -y install git

# YOU CAN UNCOMMENT NEXT LINES TO USE NODEJS
    # curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -
    # apt-get -y install nodejs
    # sudo ln -s /usr/bin/nodejs /usr/sbin/node
    # apt-get -y install npm

sudo apt-get -y install python3-pip

# Yarn
    # curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
    # echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

# Postgresql 9.4

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
sudo apt install wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add
sudo apt update
sudo apt-get -y install postgresql-9.4 postgresql-server-dev-9.4 pgadmin3 python-psycopg2

echo "local all postgres peer" > /etc/postgresql/9.4/main/pg_hba.conf
echo "local django_db django md5" >> /etc/postgresql/9.4/main/pg_hba.conf
echo "local all all peer" >> /etc/postgresql/9.4/main/pg_hba.conf
echo "host all all 127.0.0.1/32 md5" >> /etc/postgresql/9.4/main/pg_hba.conf
echo "host all all ::1/128 md5" >> /etc/postgresql/9.4/main/pg_hba.conf

service postgresql restart

sudo -u postgres bash -c "psql -c \"CREATE USER django WITH PASSWORD 'django';\""
sudo -u postgres createdb --owner=django --encoding=UTF8 django_db

# Virtualenv
pip3 install virtualenv
pip3 install virtualenvwrapper

echo "export WORKON_HOME=~/Envs" >> /home/vagrant/.profile
echo "export VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3'" >> /home/vagrant/.profile
echo "export PATH=\$PATH:/home/vagrant/django-vagrant/node_modules/.bin" >> /home/vagrant/.profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.profile
echo "cd /home/vagrant/django-vagrant/backend" >> /home/vagrant/.profile
echo "workon django-vagrant" >> /home/vagrant/.profile

su - vagrant << EOF
export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv --python=/usr/bin/python3 django-vagrant

echo "cd /home/vagrant/django-vagrant/backend" >> /home/vagrant/Envs/django-vagrant/bin/postactivate

workon django-vagrant

cd /home/vagrant/django-vagrant/

pip3 install -r requirements/dev.txt

# ACTIVATE IN CASE OF NEEDED (yarn)
# yarn install
EOF

# Redis
echo "unixsocket /var/run/redis/redis.sock" >> /etc/redis/redis.conf
echo "unixsocketperm 777" >> /etc/redis/redis.conf
echo "maxmemory 64mb" >> /etc/redis/redis.conf
sed -i.bak "s/^bind 127.0.0.1$/# bind 127.0.0.1/" /etc/redis/redis.conf
sed -i.bak "s/^port 6379$/# port 6379/" /etc/redis/redis.conf

service redis-server restart
