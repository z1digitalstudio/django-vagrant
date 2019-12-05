
db_name=django_db
db_user=django
db_password=django

sudo -u postgres dropdb $db_name
sudo -u postgres dropuser $db_user
sudo -u postgres  psql -c "CREATE USER $db_user WITH SUPERUSER PASSWORD '$db_password';"
sudo -u postgres createdb $db_name --owner=$db_user
