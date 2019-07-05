source `which virtualenvwrapper.sh`
workon django-vagrant
export PYTHONPATH=.:$PYTHONPATH
celery -A django-vagrant beat --loglevel=info
