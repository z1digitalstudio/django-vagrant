
source /home/ubuntu/venvs/django-vagrant/activate
git pull
pip install -r requirements/prod.txt
cd django-vagrant
./manage.py migrate
sudo supervisorctl -c /etc/supervisor/supervisord.conf restart all
