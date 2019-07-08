# DJANGO VAGRANT

## Dependencies

 * VirtualBox  (https://www.virtualbox.org/wiki/Downloads)
 * Vagrant (https://www.vagrantup.com/downloads.html
 
 ## Installation

    $ git clone https://github.com/z1digitalstudio/django-vagrant
    $ cd django-vagrant
    $ vagrant up --provision
 
 ## Development
 ### Create user
     $ vagrant ssh
     $ python manage.py createsuperuser
 ### Create database tables
     $ python manage.py migrate
 ### Start up 
    $ ./run.sh

## Access from the browser

 * http://localhost:8002/


## How to configure

- The base Django project lives in `backend/`
- The manage file is `backend/manage.py`
- The main settings file is `backend/settings.py`

### Environment variables

The idea is to be able to configure the project using environment variables.
This allows a more modular aproach. These variables can be set both in the host
machine or in the `.env` file.

It's recommended to set the variables in the host machine for **staging and
production** environments, so they aren't in the source code. For development,
using the `.env` file is ok to quickly test things.

These are the variables used:

| Variable | Default | What | Example |
| -------- | ------- | ---- | ------- |
| `ALLOWED_HOSTS` | | A colon separated list with the allowed hosts | `localhost:mywebsite.local` |
| `ENV` | `dev` | The current environment. When `dev`, Django `DEBUG` will be true | `dev`, `staging`, `prod`... |
| `DJANGO_SECRET_KEY` | | The secret key for Django... | |
| `DATABASE_USER` | `django` | User to connect to postgres | |
| `DATABASE_PASS` | `django` | Password to connect to postgres | |
